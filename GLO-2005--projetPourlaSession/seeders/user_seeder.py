from faker import Faker
import random
from werkzeug.security import generate_password_hash
from produit import connection

import random
from faker import Faker

fake = Faker()

def generate_random_password():
    return ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_+", k=10))


def generate_clients(connection, nb_clients):
    cursor = connection.cursor()
    clients_ids = []
    for _ in range(nb_clients):
        id_client = random.randint(1000, 9999)
        username = fake.last_name()
        email = fake.email()
        date_transaction = fake.date_between(start_date="-1y", end_date="today")
        password = generate_random_password()
        passeword_hash = generate_password_hash(password, method='pbkdf2:sha256')

        cursor.execute("CALL InsertionUtilisateurr  (%s, %s, %s, %s, NULL, TRUE, FALSE)",
                        (username, email, date_transaction, passeword_hash))
        
        clients_ids.append(id_client)  # Ajout de l'ID à la liste
    
    connection.commit()
    return clients_ids  # Retourne la liste des IDs

def generate_vendeur(connection, nb_clients):
    cursor = connection.cursor()
    clients_ids = []
    for _ in range(nb_clients):
        username = fake.last_name()
        email = fake.email()
        numero = random.randint(1000, 9999)
        date_transaction = fake.date_between(start_date="-1y", end_date="today")
        password = generate_random_password()
        passeword_hash = generate_password_hash(password, method='pbkdf2:sha256')

        cursor.execute("CALL InsertionUtilisateurr  (%s, %s, %s, %s, %s, FALSE, TRUE)",
                        (username, email, date_transaction, passeword_hash, numero))
    
    connection.commit()



if __name__ == "__main__":
    generate_clients(connection, 150)
    generate_vendeur(connection, 150)