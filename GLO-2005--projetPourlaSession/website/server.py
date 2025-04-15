'''from dotenv import load_dotenv
load_dotenv()'''
from flask import Flask, render_template, request, redirect, url_for, session, flash
#from user_model import User
import json
from flask_login import login_required, current_user
#from shared_resources import login_manager 
#from auth import auth
import pymysql
from datetime import date


from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = "mag-2005"

# Connexion à la base de données MySQL
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='Ntd.197238b',
    db='magasinenligne',
    cursorclass=pymysql.cursors.DictCursor
)

'''from database import connection, insert_Client, insert_vendeur, insert_Utilisateurs, select_user, select_livre, \
    select_Livre_by_id, select_jouet_by_id, select_Jouets, select_clients, search_users_by_query, select_user_by_email, \
    select_user_by_id, select_user_by_username, select_users_by_role, select_vendeur_name_by_jouet_id, select_vendeurs, \
    edit_jouet_by_id, edit_livre_by_id, edit_user_by_id, delete_jouet_by_id, delete_user_by_id, search_users_by_query

app = Flask(__name__)
#app.secret_key = "mag-2005"
app.register_blueprint(auth, url_prefix="/")
app.config['DB_CONNECTION'] = connection
app.config['SECRET_KEY'] = 'Ntd.197238b'
#login_manager.login_view = 'auth.login'
#login_manager.init_app(app)
'''


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM Utilisateurs WHERE username=%s AND password=%s", (username, password))
            user = cursor.fetchone()
            if user:
                session['username'] = user['username']
                session['role'] = user['role']
                return redirect(url_for('dashboard'))
            else:
                flash("Identifiants invalides.")
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'], role=session['role'])



@app.route('/ajouter-produit', methods=['GET', 'POST'])
def ajouter_produit():
    if request.method == 'POST':
        nom = request.form['nom']
        prix = float(request.form['prix'])
        description = request.form['description']
        type_produit = request.form['type']  # 'livre' ou 'jouet'

        is_jouet = type_produit.lower() == 'jouet'
        is_livre = type_produit.lower() == 'livre'

        try:
            with conn.cursor() as cursor:
                cursor.callproc('InsertionProduit', [nom, prix, description, '', is_jouet, is_livre])
            conn.commit()
            flash("Produit ajouté avec succès !")
            return redirect(url_for('dashboard'))
        except Exception as e:
            conn.rollback()
            flash(f"Erreur lors de l'ajout du produit : {str(e)}")
    return render_template('ajouter_produit.html')



@app.route('/produits')
def produits():
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM produits")
        produits = cursor.fetchall()
    return render_template('produits.html', produits=produits)


@app.route('/livres')
def livres():
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT p.*, l.nomLivre, l.prixLivre, l.descriptions 
            FROM produits p 
            JOIN Livres l ON p.idProduit = l.idLivres
        """)
        livres = cursor.fetchall()
    return render_template('livres.html', livres=livres)


@app.route('/jouets')
def jouets():
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT p.*, j.nomJouets, j.prixJouet, j.descriptions 
            FROM produits p 
            JOIN Jouets j ON p.idProduit = j.idJouets
        """)
        jouets = cursor.fetchall()
    return render_template('jouets.html', jouets=jouets)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        date_inscription = date.today()

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO Utilisateurs (username, email, password, date_inscription) VALUES (%s, %s, %s, %s)",
                    (username, email, password, date_inscription)
                )
            conn.commit()
            flash("Inscription réussie ! Vous pouvez maintenant vous connecter.")
            return redirect(url_for('login'))
        except Exception as e:
            conn.rollback()
            flash(f"Erreur lors de l'inscription : {str(e)}")

    return render_template('register.html')
    


if __name__ == '__main__':
    app.run(debug=True)
