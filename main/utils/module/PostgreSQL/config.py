import os

def config(user=None, password=None, dbname=None):
    return {
        "dbname": dbname if dbname is not None else os.getenv("POSTGRESQL_BDD_NAME"),
        "user": user if user is not None else os.getenv("POSTGRESQL_USER"),
        "password": password if password is not None else os.getenv("POSTGRESQL_PASSWORD"),
        "host": os.getenv("POSTGRESQL_HOST"),
        "port": int(os.getenv("POSTGRESQL_PORT", 5432)),
    }

def auto_connect():
    return os.getenv('POSTGRESQL_AUTO_CONNECT', 'False').lower() == 'true'
