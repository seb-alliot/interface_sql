import keyring
import os
from settings import APP_NAME

SERVICE = f"{APP_NAME}::PostgreSQL"

def config(user=None, password=None, dbname=None, host=None, port=None):
    return {
        "dbname": dbname if dbname is not None else keyring.get_password(SERVICE, "DBNAME"),
        "user": user if user is not None else keyring.get_password(SERVICE, "USER"),
        "password": password if password is not None else keyring.get_password(SERVICE, "PASSWORD"),
        "host": host if host is not None else keyring.get_password(SERVICE, "HOST"),
        "port": int(port) if port is not None else int(keyring.get_password(SERVICE, "PORT") or 5432),
    }

def auto_connect():
    return os.getenv('POSTGRESQL_AUTO_CONNECT', 'False').lower() == 'true'
