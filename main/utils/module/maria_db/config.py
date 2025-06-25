import os

def MARIA_DB_CONFIG(user=None, password=None, dbname=None):
    return {
        "database": dbname if dbname is not None else os.getenv("MARIA_DB_NAME"),
        "user": user if user is not None else os.getenv("MARIA_USER"),
        "password": password if password is not None else os.getenv("MARIA_PASSWORD"),
        "host": os.getenv("MARIA_HOST"),
        "port": int(os.getenv("MARIA_PORT", 3306)),  
    }

MARIA_DB = MARIA_DB_CONFIG()
MARIA_AUTO_CONNECT = os.getenv('MARIA_AUTO_CONNECT', 'False').lower() == 'true'  # booléen3

def maria_auto_connect():
    return os.getenv('MARIA_AUTO_CONNECT', 'False').lower() == 'true'