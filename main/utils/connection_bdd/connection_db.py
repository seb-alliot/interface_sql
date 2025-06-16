import psycopg2
from psycopg2 import OperationalError
from settings import DB_CONFIG, MAJ_DB_CONFIG, POSTGRESQL_CONFIG


def get_connection_sql(db_config):
    return psycopg2.connect(**db_config)


def connect_to_sql_database(db_config=None):
    if db_config is None:
        db_config = POSTGRESQL_CONFIG()
    try:
        connection = psycopg2.connect(**db_config)
        return connection, None
    except OperationalError as e:
        return None, str(e)




def get_connection(db_config):
    return psycopg2.connect(**db_config)


def connect_to_database(db_config=None):
    if db_config is None:
        db_config = MAJ_DB_CONFIG()
    try:
        connection = get_connection(db_config)
        return connection, None
    except OperationalError as e:
        return None, str(e)
