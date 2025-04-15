from faker import Faker
import random
from produit import connection
import random
from faker import Faker
from produit import generate_produits
from user_seeder import generate_clients



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