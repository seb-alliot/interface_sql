# imports necessary
import psycopg2, settings
from psycopg2 import OperationalError

def get_connection():
    connection = psycopg2.connect(**settings.DB_CONFIG)
    return connection

def connect_to_database():
    try:
        connection = get_connection()
        return connection, None
    except OperationalError as e:
        return None, str(e)


# code/fonction/exemple.py

def message_bienvenu(nom):

    return f"Bonjour {nom} ! Bienvenue 😊"
