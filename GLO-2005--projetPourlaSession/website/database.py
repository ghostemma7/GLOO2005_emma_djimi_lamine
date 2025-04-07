import ast
from collections import defaultdict

import pymysql
import os
from dotenv import load_dotenv
import pymysql.cursors
import random
from werkzeug.security import generate_password_hash

from flask import json

load_dotenv()

connection = pymysql.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USERNAME'),
    password=os.getenv('DB_PASSWORD'),
    db=os.getenv('DB_DATABASE'),
    port=int(os.getenv('DB_PORT')),
    autocommit=True,
    cursorclass=pymysql.cursors.DictCursor
)

cursor = connection.cursor()

def insert_Client(username, email, password, date_inscription):
    password = generate_password_hash(password, method='pbkdf2:sha256')
    query = "CALL InsertionUtilisateurs (%s, %s, %s, %s, NULL, FALSE, FALSE)"  # Ajout de %s pour la date
    cursor.execute(query, (username, email, password, date_inscription))  # Ajout de date_inscription
    connection.commit()

def insert_vendeur(username, email, password, date_inscription, numero):
    password = generate_password_hash(password, method='pbkdf2:sha256')
    query = "CALL InsertionUtilisateurs (%s, %s, %s, %s, %s, FALSE, FALSE)"  # Ajout de %s pour la date
    cursor.execute(query, (username, email, password, date_inscription, numero))  # Ajout de date_inscription
    connection.commit()

def insert_Utilisateurs(username, email, date_inscription, password, role='User'):
    query = "INSERT INTO Utilisateurs (username, email, date_inscription, password, role) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (username, password, email, role))

def select_user():
    request = "SELECT id, username, email, date_inscription, role FROM magasinenligne1.Utilisateurs;"
    cursor.execute(request)
    utilisateurs = cursor.fetchall()
    return utilisateurs

def select_livre():
    request = "SELECT idLivres, nomLivre, prixLivre, descriptions FROM magasinenligne1.Livres;"
    cursor.execute(request)
    livre = cursor.fetchall()
    return livre

def select_Livre_by_id(Livre_id):
    query = "SELECT * FROM Chansons WHERE idLivres = %s;"
    cursor.execute(query, (Livre_id,))
    Jouet_data = cursor.fetchone()
    return Jouet_data

def select_Jouets():
    request = "SELECT idJouets, nomJouets, prixJouet, descriptions FROM magasinenligne1.Jouets;"
    cursor.execute(request)
    livre = cursor.fetchall()
    return livre

def select_jouet_by_id(jouet_id):
    query = "SELECT * FROM Chansons WHERE idJouets = %s;"
    cursor.execute(query, (jouet_id,))
    Jouet_data = cursor.fetchone()
    return Jouet_data

def edit_livre_by_id(livre_id, nom_livre, prix_livre, description, utilisateur_id):

    try:
        # Vérifier si le livre existe et si l'utilisateur a le droit de le modifier
        query = "SELECT COUNT(*) FROM Livres WHERE idLivres = %s AND utilisateur_id = %s"
        cursor.execute(query, (livre_id, utilisateur_id))
        count = cursor.fetchone()[0]

        if count == 0:
            raise Exception("Le livre n'existe pas ou vous n'avez pas le droit de le modifier.")

        # Mettre à jour les informations du livre
        query = "UPDATE Livres SET nomLivre = %s, prixLivre = %s, description = %s WHERE idLivre = %s"
        cursor.execute(query, (nom_livre, prix_livre, description, livre_id))
        connection.commit()

        return True  # Indiquer que la modification a réussi

    except Exception as e:
        print(f"Erreur lors de la modification du jouet : {e}")
        return False  # Indiquer que la modification a échoué

def edit_jouet_by_id(jouet_id, nom_jouet, prix_jouet, description, utilisateur_id):

    try:
        # Vérifier si le jouet existe et si l'utilisateur a le droit de le modifier
        query = "SELECT COUNT(*) FROM Jouets WHERE idJouets = %s AND utilisateur_id = %s"
        cursor.execute(query, (jouet_id, utilisateur_id))
        count = cursor.fetchone()[0]

        if count == 0:
            raise Exception("Le jouet n'existe pas ou vous n'avez pas le droit de le modifier.")

        # Mettre à jour les informations du jouet
        query = "UPDATE Jouets SET nomJouets = %s, prixJouets = %s, description = %s WHERE idJouets = %s"
        cursor.execute(query, (nom_jouet, prix_jouet, description, jouet_id))
        connection.commit()

        return True  # Indiquer que la modification a réussi

    except Exception as e:
        print(f"Erreur lors de la modification du jouet : {e}")
        return False  # Indiquer que la modification a échoué