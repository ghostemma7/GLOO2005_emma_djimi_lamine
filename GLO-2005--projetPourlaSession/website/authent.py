from flask_login import login_user, logout_user, login_required, current_user
from flask import Blueprint, render_template, request, current_app, redirect, url_for, flash
import pymysql, pymysql.cursors
from database import select_user_by_username, select_user_by_email, insert_vendeur, insert_client
from user_model import load_user
import re
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        user_data = select_user_by_username(username)
        if (user_data and check_password_hash(user_data['password'], password)) or (
                user_data and user_data['password'] == password):
            user = load_user(user_data['id'])
            login_user(user, remember=True)
            return redirect(url_for('dashboard'))
        else:
            flash("Nom d'utilisateur ou mot de passe invalide", category='error')
            return redirect(url_for('index'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        email = request.form.get("email")
        username_exists = select_user_by_username(username)
        email_exists = select_user_by_email(email)

        if username_exists:
            flash("Le nom d'utilisateur existe déjà", category='error')
        elif email_exists:
            flash("L'email existe déjà", category='error')
        elif password1 != password2:
            flash("Les mots de passe ne correspondent pas", category='error')
        elif len(username) < 4:
            flash("Le nom d'utilisateur doit comporter au moins 4 caractères", category='error')
        elif len(password1) < 8:
            flash("Le mot de passe doit comporter au moins 8 caractères", category='error')
        elif len(email) < 10:
            flash("L'email doit comporter au moins 10 caractères", category='error')
        elif not is_valid_email(email):
            flash("Email invalide", category='error')
        else:
            insert_vendeur(username, email, generate_password_hash(password1, method='pbkdf2:sha256'))
            user_data = select_user_by_email(email)
            user = load_user(user_data['id'])
            login_user(user, remember=True)
            return redirect(url_for("dashboard"))

    return render_template("sign-up.html")


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))