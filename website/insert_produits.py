import pymysql
from random import randint, uniform

# Connexion à la base de données
conn = pymysql.connect(
    host='localhost',
    user='root',  # ou un autre utilisateur MySQL
    password='Ntd.197238b',  
    db='magasinenligne',
    cursorclass=pymysql.cursors.DictCursor
)

with conn.cursor() as cursor:
    for i in range(1, 101):
        nom = f"Produit {i}"
        prix = round(uniform(10.0, 200.0), 2)
        description = f"Description automatique pour le produit {i}"
        cursor.execute(
            "INSERT INTO produits (nomProduits, prixProduit, descriptions) VALUES (%s, %s, %s)",
            (nom, prix, description)
        )

conn.commit()
