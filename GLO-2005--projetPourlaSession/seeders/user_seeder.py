from faker import Faker
import random
from werkzeug.security import generate_password_hash
from produit import connection

import random
from faker import Faker

fake = Faker()

def generate_random_password(length=10):
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return ''.join(random.choices(characters, k=length))

def generate_clients(connection, nb_clients):
    cursor = connection.cursor()
    clients_ids = []

    for _ in range(nb_clients):
        username = fake.last_name()  # chaîne de caractères
        email = fake.email()
        date_transaction = fake.date_between(start_date="-1y", end_date="today")
        password = generate_random_password()
        passeword_hash = generate_password_hash(password, method='pbkdf2:sha256')

        # Appel correct avec 7 paramètres
        cursor.execute(
            "CALL InsertionUtilisateurr(%s, %s, %s, %s, %s, %s, %s)",
            (username, email, date_transaction, passeword_hash, None, True, False)
        )
        result = cursor.fetchone()
        if result:
            last_id = result["id"]  # ou result['id'] si DictCursor
            clients_ids.append(last_id)
        else:
            print(" Aucun ID retourné pour l'utilisateur :", username)

    connection.commit()
    return clients_ids


def generate_vendeur(connection, nb_vendeurs):
    cursor = connection.cursor()
    vendeurs_ids = []

    for _ in range(nb_vendeurs):
        username = fake.last_name()
        email = fake.email()
        numero = random.randint(1000, 9999)
        date_transaction = fake.date_between(start_date="-1y", end_date="today")
        password = generate_random_password()
        passeword_hash = generate_password_hash(password, method='pbkdf2:sha256')

        # Appel de la procédure
        cursor.execute(
            "CALL InsertionUtilisateurr(%s, %s, %s, %s, %s, %s, %s)",
            (username, email, date_transaction, passeword_hash, numero, False, True)
        )

        # Récupération du user_id retourné par la procédure
        result = cursor.fetchone()
        if result:
            last_id = result["id"]  # ou result["id"] avec DictCursor
            vendeurs_ids.append(last_id)
        else:
            print(" Aucun ID retourné pour le vendeur :", username)

    connection.commit()
    return vendeurs_ids

if __name__ == "__main__":
    generate_clients(connection, 150)
    generate_vendeur(connection, 150)