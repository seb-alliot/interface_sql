import os
from dotenv import load_dotenv
load_dotenv()

import keyring
from settings import APP_NAME

SERVICE = f"{APP_NAME}::MongoDB"

def config(user=None, password=None, dbname=None, host=None, port=None):
    user = user or keyring.get_password(SERVICE, "USER")
    password = password or keyring.get_password(SERVICE, "PASSWORD")
    host = host or keyring.get_password(SERVICE, "HOST")
    dbname = dbname or keyring.get_password(SERVICE, "DBNAME")
    port = port or keyring.get_password(SERVICE, "PORT") or "27017"

    uri = f"mongodb+srv://{user}:{password}@{host}/?retryWrites=true&w=majority"

    return {
        "database": dbname,
        "user": user,
        "password": password,
        "host": host,
        "port": int(port),
        "uri": uri,
    }

# Paramètres principaux
MONGODB_BDD_NAME = keyring.get_password(SERVICE, "DBNAME")
MONGODB_USER = keyring.get_password(SERVICE, "USER")
MONGODB_PASSWORD = keyring.get_password(SERVICE, "PASSWORD")
MONGODB_HOST = keyring.get_password(SERVICE, "HOST")

# URI MongoDB complète
MONGO_URI = (
    f"mongodb+srv://{MONGODB_USER}:{MONGODB_PASSWORD}@{MONGODB_HOST}/"
    f"?retryWrites=true&w=majority"
)

# Fonction booléenne propre pour l'autoconnect
def auto_connect():
    return os.getenv('MONGODB_AUTO_CONNECT', 'False').strip().lower() in ('true', '1', 'yes')

# Variable booléenne globale
MONGODB_AUTO_CONNECT = auto_connect()

# Dictionnaire global
MONGO_DB = config()