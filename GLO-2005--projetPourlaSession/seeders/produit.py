from faker import Faker
import random
from dotenv import load_dotenv
import pymysql
import os

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

def generate_produits(connection, nb_produits):
    fake = Faker()
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
    generate_produits(connection, 150)