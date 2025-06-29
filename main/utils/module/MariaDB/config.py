import os

def config(user=None, password=None, dbname=None):
    return {
        "database": dbname if dbname is not None else os.getenv("MARIA_DB_NAME"),
        "user": user if user is not None else os.getenv("MARIA_USER"),
        "password": password if password is not None else os.getenv("MARIA_PASSWORD"),
        "host": os.getenv("MARIA_HOST"),
        "port": int(os.getenv("MARIA_PORT", 3306)),
    }

def auto_connect():
    return os.getenv('MARIA_AUTO_CONNECT', 'False').lower() == 'true'