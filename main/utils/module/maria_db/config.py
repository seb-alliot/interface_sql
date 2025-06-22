import os

def MARIA_DB_CONFIG(user=None, password=None, dbname=None):
    return {
        "user": user if user is not None else os.getenv("MARIA_USER"),
        "password": password if password is not None else os.getenv("MARIA_PASSWORD"),
        "host": os.getenv("MARIA_HOST"),
        "port": int(os.getenv("MARIA_PORT")),
    }

MARIA_DB = MARIA_DB_CONFIG()
MARIA_AUTO_CONNECT = os.getenv('MARIA_AUTO_CONNECT', 'False').lower() == 'true'  # booléen