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

def insert_client(id, nom, prenom, adresse, telephone, email, date_transaction):
    query = "INSERT Client (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (id, nom, prenom, adresse, telephone, email, date_transaction))


