from dotenv import load_dotenv
load_dotenv()

import os
import sys
import logging
from datetime import date
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
import pymysql
from pymysql import MySQLError
from werkzeug.security import generate_password_hash, check_password_hash

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")  # Clé secrète à définir dans le fichier .env

# Connexion à la base de données
def get_db_connection():
    try:
        return pymysql.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD"),
            db=os.getenv("DB_NAME", "magasinenligne"),
            cursorclass=pymysql.cursors.DictCursor
        )
    except MySQLError as e:
        logging.error(f"Erreur de connexion à la base de données: {e}")
        return None

# Middleware de login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash("Veuillez vous connecter pour accéder à cette page.")
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        logging.error(f"Erreur dans la route index: {str(e)}")
        abort(500)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash("Tous les champs sont obligatoires.")
            return render_template('login.html')

        conn = get_db_connection()
        if not conn:
            flash("Erreur de connexion à la base de données.")
            return render_template('login.html')

        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Utilisateurs WHERE username=%s", (username,))
                user = cursor.fetchone()

                if user and check_password_hash(user['password'], password):
                    session['username'] = user['username']
                    session['role'] = user['role']
                    session['user_id'] = user['id']
                    flash("Connexion réussie !")
                    return redirect(url_for('dashboard'))
                else:
                    flash("Identifiants invalides.")
        except MySQLError as e:
            logging.error(f"Erreur SQL: {str(e)}")
            flash("Erreur lors de la connexion.")
        finally:
            conn.close()

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Déconnexion réussie.")
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=session['username'], role=session['role'])

@app.route('/ajouter-produit', methods=['GET', 'POST'])
@login_required
def ajouter_produit():
    if request.method == 'POST':
        nom = request.form.get('nom')
        prix = request.form.get('prix')
        description = request.form.get('description')
        type_produit = request.form.get('type')

        if not all([nom, prix, description, type_produit]):
            flash("Tous les champs sont obligatoires.")
            return render_template('ajouter_produit.html')

        try:
            prix = float(prix)
        except ValueError:
            flash("Le prix doit être un nombre.")
            return render_template('ajouter_produit.html')

        is_jouet = type_produit.lower() == 'jouet'
        is_livre = type_produit.lower() == 'livre'

        conn = get_db_connection()
        if not conn:
            flash("Erreur de connexion à la base de données.")
            return render_template('ajouter_produit.html')

        try:
            with conn.cursor() as cursor:
                # ⚠️ Assurez-vous que cette procédure stockée attend bien ces paramètres
                cursor.callproc('InsertionProduit', [nom, prix, description, '', is_jouet, is_livre])
            conn.commit()
            flash("Produit ajouté avec succès !")
            return redirect(url_for('dashboard'))
        except MySQLError as e:
            conn.rollback()
            logging.error(f"Erreur SQL: {str(e)}")
            flash("Erreur lors de l'ajout du produit.")
        finally:
            conn.close()

    return render_template('ajouter_produit.html')

@app.route('/produits')
@login_required
def produits():
    conn = get_db_connection()
    if not conn:
        abort(500)

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM produits")
            produits = cursor.fetchall()
        return render_template('produits.html', produits=produits)
    finally:
        conn.close()

@app.route('/livres')
@login_required
def livres():
    conn = get_db_connection()
    if not conn:
        abort(500)

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT p.*, l.nomLivre, l.prixLivre, l.descriptions 
                FROM produits p 
                JOIN Livres l ON p.idProduit = l.idProduit
            """)
            livres = cursor.fetchall()
        return render_template('livres.html', livres=livres)
    finally:
        conn.close()

@app.route('/jouets')
@login_required
def jouets():
    conn = get_db_connection()
    if not conn:
        abort(500)

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT p.*, j.nomJouets, j.prixJouet, j.descriptions 
                FROM produits p 
                JOIN Jouets j ON p.idProduit = j.idProduit
            """)
            jouets = cursor.fetchall()
        return render_template('jouets.html', jouets=jouets)
    finally:
        conn.close()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        date_inscription = date.today()

        if not all([username, email, password, confirm_password]):
            flash("Tous les champs sont obligatoires.")
            return render_template('register.html')

        if password != confirm_password:
            flash("Les mots de passe ne correspondent pas.")
            return render_template('register.html')

        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        if not conn:
            flash("Erreur de connexion à la base de données.")
            return render_template('register.html')

        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Utilisateurs WHERE username = %s OR email = %s", (username, email))
                if cursor.fetchone():
                    flash("Un utilisateur avec ce nom ou cet email existe déjà.")
                    return render_template('register.html')

                cursor.execute(
                    "INSERT INTO Utilisateurs (username, email, password, date_inscription) VALUES (%s, %s, %s, %s)",
                    (username, email, hashed_password, date_inscription)
                )
            conn.commit()
            flash("Inscription réussie ! Vous pouvez vous connecter.")
            return redirect(url_for('login'))
        except MySQLError as e:
            conn.rollback()
            logging.error(f"Erreur SQL lors de l'inscription: {str(e)}")
            flash("Erreur lors de l'inscription.")
        finally:
            conn.close()

    return render_template('register.html')

# Gestion des erreurs
@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(404)
@app.errorhandler(500)
def handle_error(error):
    return render_template('error.html', error=error), error.code


if __name__ == '__main__':
    app.run(debug=True)
