import os
from dotenv import load_dotenv
load_dotenv()

def config(user=None, password=None, dbname=None):
    user = user or os.getenv("MONGODB_USER")
    password = password or os.getenv("MONGODB_PASSWORD")
    host = os.getenv("MONGODB_HOST")
    dbname = dbname or os.getenv("MONGODB_BDD_NAME")

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
MONGODB_BDD_NAME = os.getenv("MONGODB_BDD_NAME")
MONGODB_USER = os.getenv("MONGODB_USER")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
MONGODB_HOST = os.getenv("MONGODB_HOST")

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