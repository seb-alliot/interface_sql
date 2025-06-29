import os

def config(user=None, password=None, dbname=None):
    return {
        "database": dbname if dbname is not None else os.getenv("MARIADB_BDD_NAME"),
        "user": user if user is not None else os.getenv("MARIADB_USER"),
        "password": password if password is not None else os.getenv("MARIADB_PASSWORD"),
        "host": os.getenv("MARIADB_HOST"),
        "port": int(os.getenv("MARIADB_PORT", 3306)),
    }

def auto_connect():
    return os.getenv('MARIADB_AUTO_CONNECT', 'False').lower() == 'true'