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
        nom_produit = fake.word().capitalize() + " " + random.choice(["Pro", "Max", "Plus", "Ultra", "X"])
        categorie = random.choice(categories)
        prix = round(random.uniform(5.0, 500.0), 2)

        if categorie == "Jouets":
            description = "jouet pour enfants"
            is_jouet = True
            is_livre = False
        else:
            description = "livre intéressant"
            is_jouet = False
            is_livre = True

        cursor.execute(
            "CALL InsertionProduits(%s, %s, %s, %s, %s)",
            (nom_produit, prix, description, is_jouet, is_livre)
        )

        result = cursor.fetchone()
        if result:
            last_id = result["id"]  # ou result['id']
            produits_ids.append(last_id)
        else:
            print("Aucun ID retourné pour produit :", nom_produit)

    connection.commit()
    return produits_ids


if __name__ == "__main__":
    generate_produits(connection, 150)