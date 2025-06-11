import psycopg2
import settings



def get_connection():
    return psycopg2.connect(**settings.DB_CONFIG)


def connect_to_database():
    connection = get_connection()
    cursor = connection.cursor()
    return connection, cursor
