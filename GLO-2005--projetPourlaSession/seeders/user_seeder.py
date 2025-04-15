from faker import Faker
import random
from werkzeug.security import generate_password_hash
from produit import connection
import uuid

import random
from faker import Faker

fake = Faker()

def generate_random_password(length=10):
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return ''.join(random.choices(characters, k=length))

def generate_clients(connection, nb_clients):
    cursor = connection.cursor()
    clients_ids = []
    used_emails = set()  # Pour s'assurer que les e-mails sont uniques

    for _ in range(nb_clients):
        username = fake.last_name()
        
        # Génération d'un e-mail unique
        email_base = username.lower()
        email = f"{email_base}.{uuid.uuid4().hex[:8]}@example.com"
        while email in used_emails:
            email = f"{email_base}.{uuid.uuid4().hex[:8]}@example.com"
        used_emails.add(email)

        date_transaction = fake.date_between(start_date="-1y", end_date="today")
        password = generate_random_password()
        password_hash = generate_password_hash(password, method='pbkdf2:sha256')

        # Appel de la procédure stockée
        cursor.execute(
            "CALL InsertionUtilisateurs(%s, %s, %s, %s, %s, %s, %s)",
            (username, email, date_transaction, password_hash, None, True, False)
        )
        
        result = cursor.fetchone()
        if result:
            last_id = result["id"]  # ou result['id'] si DictCursor
            clients_ids.append(last_id)
        else:
            print("Aucun ID retourné pour l'utilisateur :", username)

    connection.commit()
    return clients_ids


def generate_vendeur(connection, nb_vendeurs):
    cursor = connection.cursor()
    vendeurs_ids = []
    used_emails = set()  # Pour garantir unicité

    for _ in range(nb_vendeurs):
        username = fake.last_name()

        # Génération d’un e-mail unique
        email_base = username.lower()
        email = f"{email_base}.{uuid.uuid4().hex[:8]}@example.com"
        while email in used_emails:
            email = f"{email_base}.{uuid.uuid4().hex[:8]}@example.com"
        used_emails.add(email)

        numero = random.randint(1000, 9999)
        date_transaction = fake.date_between(start_date="-1y", end_date="today")
        password = generate_random_password()
        password_hash = generate_password_hash(password, method='pbkdf2:sha256')

        # Appel de la procédure stockée
        cursor.execute(
            "CALL InsertionUtilisateurs(%s, %s, %s, %s, %s, %s, %s)",
            (username, email, date_transaction, password_hash, numero, False, True)
        )

        result = cursor.fetchone()
        if result:
            last_id = result["id"]
            vendeurs_ids.append(last_id)
        else:
            print("Aucun ID retourné pour le vendeur :", username)

    connection.commit()
    return vendeurs_ids

if __name__ == "__main__":
    generate_clients(connection, 150)
    generate_vendeur(connection, 150)