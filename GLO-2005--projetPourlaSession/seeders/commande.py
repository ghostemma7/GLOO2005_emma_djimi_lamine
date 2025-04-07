from faker import Faker
import random
from dotenv import load_dotenv
import pymysql
import os
import datetime
from user_seeder import generate_produits, generate_clients

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

def insert_random_commande(connection, commande):
    cursor = connection.cursor()
    fake = Faker()
    clients_ids = generate_clients(100)  # Récupère les IDs des clients
    produits_ids = generate_produits(150) # Récupère les IDs des produits

    for _ in range(commande):
        id_commande = random.randint(10000, 19999)
        id_client = random.choice(clients_ids)
        id_produit = random.choice(produits_ids)
        quantite = random.randint(1, 5)
        prix_unitaire = round(random.uniform(5.0, 500.0), 2)
        cout_total = quantite * prix_unitaire
        date_commande = fake.date_between(start_date="-1y", end_date="today")

        cursor.execute(f"INSERT INTO Commandes (id_commande, id_client, id_produit, quantite, cout_total, date_commande) " \
                f"VALUES ({id_commande}, {id_client}, {id_produit}, {quantite}, {cout_total}, '{date_commande}');")

if __name__ == "__main__":
    insert_random_commande(connection, 100)