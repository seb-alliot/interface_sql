import os
from dotenv import load_dotenv
load_dotenv()

def MONGO_DB_CONFIG(user=None, password=None, dbname=None):
    user = user or os.getenv("MONGO_USER")
    password = password or os.getenv("MONGO_PASSWORD")
    host = os.getenv("MONGO_HOST")
    dbname = dbname or os.getenv("MONGO_NAME")

    uri = f"mongodb+srv://{user}:{password}@{host}/?retryWrites=true&w=majority"

    return {
        "database": dbname,
        "user": user,
        "password": password,
        "host": host,
        "port": int(os.getenv("MONGO_PORT", 27017)),
        "uri": uri,
    }


# Paramètres principaux
MONGO_NAME = os.getenv("MONGO_NAME")
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_HOST = os.getenv("MONGO_HOST")

# URI MongoDB complète
MONGO_URI = (
    f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}/"
    f"?retryWrites=true&w=majority"
)

# Fonction booléenne propre pour l'autoconnect
def mongo_auto_connect():
    return os.getenv('MONGO_AUTO_CONNECT', 'False').strip().lower() in ('true', '1', 'yes')

# Variable booléenne globale
MONGO_AUTO_CONNECT = mongo_auto_connect()

# Dictionnaire global
MONGO_DB = MONGO_DB_CONFIG()


