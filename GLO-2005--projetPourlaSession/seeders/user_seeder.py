from faker import Faker
import random
from werkzeug.security import generate_password_hash
from commande import connection

import random
from faker import Faker

fake = Faker()

def generate_clients(connection, nb_clients):
    cursor = connection.cursor()
    clients_ids = []
    for _ in range(nb_clients):
        id_client = random.randint(1000, 9999)
        nom = fake.last_name()
        prenom = fake.first_name()
        adresse = fake.address().replace("\n", ", ")
        telephone = fake.phone_number()
        email = fake.email()
        date_transaction = fake.date_between(start_date="-1y", end_date="today")

        cursor.execute(f"INSERT INTO Clients (id, nom, prenom, adresse, telephone, email, date_transaction) " \
                f"VALUES ({id_client}, '{nom}', '{prenom}', '{adresse}', '{telephone}', '{email}', '{date_transaction}');")
        
        clients_ids.append(id_client)  # Ajout de l'ID à la liste
    
    connection.commit()
    return clients_ids  # Retourne la liste des IDs



def generate_produits(connection, nb_produits):
    produits_ids = []
    categories = ["Jouets", "Livres"]
    cursor = connection.cursor()
    for _ in range(nb_produits):
        id_produit = random.randint(1000, 9999)
        nom_produit = fake.word().capitalize() + " " + random.choice(["Pro", "Max", "Plus", "Ultra", "X"])
        categorie = random.choice(categories)
        prix = round(random.uniform(5.0, 500.0), 2)

        cursor.execute(f"INSERT INTO produits (id, nom, categorie, prix) " \
                f"VALUES ({id_produit}, '{nom_produit}', '{categorie}', {prix});")
        
        produits_ids.append(id_produit)  # Ajout de l'ID à la liste


    connection.commit()
    return produits_ids  # Retourne la liste des IDs

if __name__ == "__main__":
    clients_ids = generate_clients(connection, 100)
    produits_ids = generate_produits(connection, 150)
    
