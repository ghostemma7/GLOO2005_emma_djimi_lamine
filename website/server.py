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
app.secret_key = 'Ntd.197238b'

# Connexion à la base de données
def get_db_connection():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='Ntd.197238b',
            database='magasinenligne',
            port=3306,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        logging.info("Connexion à la DB établie avec succès")
        return conn
    except pymysql.MySQLError as e:
        logging.error(f"Échec de connexion à MySQL: Code {e.args[0]} - {e.args[1]}")
        return None
    except Exception as e:
        logging.error(f"Erreur inattendue: {str(e)}")
        return None

# Décorateur pour vérifier la connexion
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Veuillez vous connecter pour accéder à cette page.")
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Décorateur pour vérifier le rôle
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'role' not in session or session['role'] != role:
                flash("Accès refusé : permissions insuffisantes.")
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/')
def accueil():
    try:
        return render_template('index.html')
    except Exception as e:
        logging.error(f"Erreur dans la route accueil: {str(e)}")
        abort(500)


@app.route('/connexion', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Debug: Afficher les valeurs reçues
        print(f"Tentative de connexion - Username: {username}, Password: {password}")

        if not username or not password:
            flash("Tous les champs sont obligatoires.")
            return render_template('login.html')

        conn = get_db_connection()
        if not conn:
            flash("Erreur de connexion à la base de données.")
            return render_template('login.html')

        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM Utilisateurs WHERE username = %s", (username,))
                user = cursor.fetchone()
                
                # Debug: Afficher l'utilisateur trouvé
                print(f"Utilisateur trouvé: {user}")

                if user and check_password_hash(user['password'], password):
                    # Initialisation de session CRITIQUE
                    session['user_id'] = user['id']
                    session['username'] = user['username']
                    session['role'] = user['role']
                    session['logged_in'] = True  # Nouveau flag important
                    
                    # Debug: Confirmation session
                    print(f"Session après login: {session}")

                    flash("Connexion réussie !", 'success')
                    return redirect(url_for('dashboard'))  # Redirection vers le dashboard
                else:
                    flash("Identifiants incorrects.", 'danger')
        except MySQLError as e:
            logging.error(f"Erreur SQL: {str(e)}")
            flash("Erreur lors de la connexion.", 'danger')
        finally:
            conn.close()

    return render_template('login.html')

@app.route('/deconnexion')
def logout():
    session.clear()
    flash("Vous avez été déconnecté avec succès.")
    return redirect(url_for('accueil'))

@app.route('/tableau-de-bord')
@login_required
def dashboard():
    return render_template('dashboard.html', 
                         username=session['username'], 
                         role=session['role'],
                         vendeur_num=session.get('vendeur_num'))

@app.route('/ajouter-produit', methods=['GET', 'POST'])
@login_required
@role_required('Vendeur')
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
            flash("Le prix doit être un nombre valide.")
            return render_template('ajouter_produit.html')

        is_jouet = type_produit.lower() == 'jouet'
        is_livre = type_produit.lower() == 'livre'

        conn = get_db_connection()
        if not conn:
            flash("Erreur de connexion à la base de données.")
            return render_template('ajouter_produit.html')

        try:
            with conn.cursor() as cursor:
                # Appel de la procédure stockée corrigée
                cursor.callproc('InsertionProduit', [
                    nom, 
                    prix, 
                    description, 
                    type_produit.capitalize(), 
                    is_jouet, 
                    is_livre
                ])
                conn.commit()
                
                # Lier le produit au vendeur
                cursor.execute("""
                    INSERT INTO ProduitsVendeurs (idProduit, idVendeur) 
                    VALUES (LAST_INSERT_ID(), %s)
                """, (session['user_id'],))
                conn.commit()
                
                flash("Produit ajouté avec succès !")
                return redirect(url_for('mes_produits'))
        except MySQLError as e:
            conn.rollback()
            logging.error(f"Erreur SQL: {str(e)}")
            flash(f"Erreur lors de l'ajout du produit: {str(e)}")
        finally:
            conn.close()

    return render_template('ajouter_produit.html')

@app.route('/mes-produits')
@login_required
@role_required('Vendeur')
def mes_produits():
    conn = get_db_connection()
    if not conn:
        abort(500)

    try:
        with conn.cursor() as cursor:
            # Récupérer les produits du vendeur connecté
            cursor.execute("""
                SELECT p.* 
                FROM produits p
                JOIN ProduitsVendeurs pv ON p.idProduit = pv.idProduit
                WHERE pv.idVendeur = %s
            """, (session['user_id'],))
            produits = cursor.fetchall()
            
            # Séparer les jouets et livres
            jouets = []
            livres = []
            
            for produit in produits:
                if produit['role'] == 'Jouet':
                    cursor.execute("SELECT * FROM Jouets WHERE idJouets = %s", (produit['idProduit'],))
                    jouet = cursor.fetchone()
                    if jouet:
                        jouets.append({**produit, **jouet})
                elif produit['role'] == 'Livre':
                    cursor.execute("SELECT * FROM Livres WHERE idLivres = %s", (produit['idProduit'],))
                    livre = cursor.fetchone()
                    if livre:
                        livres.append({**produit, **livre})
            
        return render_template('mes_produits.html', 
                            jouets=jouets, 
                            livres=livres)
    except MySQLError as e:
        logging.error(f"Erreur SQL: {str(e)}")
        abort(500)
    finally:
        conn.close()

@app.route('/inscription', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Debug: Affiche les données reçues
        print("Données du formulaire:", request.form)
        
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role = request.form.get('role', 'Client')
        numero_vendeur = request.form.get('numero_vendeur')

        # Validation basique
        if not all([username, email, password, confirm_password]):
            flash("Tous les champs sont obligatoires", "error")
            return render_template('register.html')

        if password != confirm_password:
            flash("Les mots de passe ne correspondent pas", "error")
            return render_template('register.html')

        if role == 'Vendeur' and not numero_vendeur:
            flash("Le numéro de vendeur est obligatoire", "error")
            return render_template('register.html')

        # Connexion DB
        conn = get_db_connection()
        if not conn:
            flash("Erreur de base de données", "error")
            return render_template('register.html')

        try:
            with conn.cursor() as cursor:
                # Vérifie si l'utilisateur existe déjà
                cursor.execute("SELECT * FROM Utilisateurs WHERE username = %s OR email = %s", (username, email))
                if cursor.fetchone():
                    flash("Un utilisateur avec ce nom ou email existe déjà", "error")
                    return render_template('register.html')

                # Hash du mot de passe
                hashed_pw = generate_password_hash(password)
                
                # Insertion
                cursor.execute(
                    "INSERT INTO Utilisateurs (username, email, password, role) VALUES (%s, %s, %s, %s)",
                    (username, email, hashed_pw, role)
                )
                
                # Insertion spécifique au rôle
                user_id = cursor.lastrowid
                if role == 'Vendeur':
                    cursor.execute(
                        "INSERT INTO Vendeurs (idVendeur, numeroduVendeur) VALUES (%s, %s)",
                        (user_id, numero_vendeur)
                    )
                
                conn.commit()
                flash("Inscription réussie! Vous pouvez maintenant vous connecter", "success")
                return redirect(url_for('login'))

        except Exception as e:
            conn.rollback()
            print("Erreur lors de l'inscription:", str(e))
            flash("Une erreur est survenue lors de l'inscription", "error")
            return render_template('register.html')
            
        finally:
            conn.close()

    return render_template('register.html')

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

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
        # Conversion en booléen pour la procédure stockée
        is_jouet = categorie.lower() == 'jouet'
        is_livre = categorie.lower() == 'livre'

        conn = get_db_connection()
        if not conn:
            flash("Erreur de connexion à la base de données.")
            return render_template('add-product.html')

        try:
            with conn.cursor() as cursor:
                cursor.callproc('InsertionProduit', [
                    nom, 
                    prix, 
                    description, 
                    categorie.capitalize(), 
                    is_jouet, 
                    is_livre
                ])
                conn.commit()
                flash("Produit ajouté avec succès !")
                return redirect(url_for('produits'))
        except MySQLError as e:
            conn.rollback()
            logging.error(f"Erreur SQL: {str(e)}")
            flash(f"Erreur lors de l'ajout du produit: {str(e)}")
        finally:
            conn.close()

    return render_template('add-product.html')

# Gestion des erreurs
# Remplacer la fonction gestion_erreur existante par :
@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(404)
@app.errorhandler(500)
def gestion_erreur(error):
    return f"""
    <h1>{error.code} - {error.name}</h1>
    <p>{error.description}</p>
    <a href="{url_for('accueil')}">Retour à l'accueil</a>
    """, error.code
if __name__ == '__main__':
    app.run(debug=True)