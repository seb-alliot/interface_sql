# imports necessary
import psycopg2, settings
from psycopg2 import OperationalError
from settings import DB_CONFIG

def get_connection(DB_CONFIG):
    return psycopg2.connect(**DB_CONFIG)

def connect_to_database(DB_CONFIG=settings.DB_CONFIG):
    try:
        connection = get_connection(DB_CONFIG)  
        return connection, None
    except OperationalError as e:
        return None, str(e)