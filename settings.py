import os
import sys
from dotenv import load_dotenv

# Chemin du dossier de l'exécutable (ou script en dev)
base_path = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
load_dotenv(dotenv_path=os.path.join(base_path, '.env'))


APP_SECRET = os.getenv('APP_SECRET')

APP_NAME = "Interface SQL"
VERSION = "version alpha 0.1.0"

def MAJ_DB_CONFIG(user=None, password=None):

    return {
        'dbname': os.getenv('DB_NAME'),
        'user': user if user is not None else os.getenv('DB_USER'),
        'password': password if password is not None else os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT'),
    }
DB_CONFIG = MAJ_DB_CONFIG()
DB_AUTO_CONNECT =  os.getenv('DB_AUTO_CONNECT', 'False').lower() == 'true'


def POSTGRESQL_CONFIG(user=None, password=None, dbname=None):
    return {
        "dbname": dbname if dbname is not None else os.getenv("POSTGRESQL_NAME"),
        "user": user if user is not None else os.getenv("POSTGRESQL_USER"),
        "password": password if password is not None else os.getenv("POSTGRESQL_PASSWORD"),
        "host": os.getenv("POSTGRESQL_HOST"),
        "port": int(os.getenv("POSTGRESQL_PORT")),
    }

POSTGRES_DB = POSTGRESQL_CONFIG()
# On convertis la variable d'environnement en booléen, car un str n'est pas un booléen mais une chaîne de caractères
# on fait donc une comparaison pour renvoyer tru ou false
POSTGRESQL_AUTO_CONNECT = os.getenv('POSTGRESQL_AUTO_CONNECT', 'False').lower() == 'true'  # booléen

def MARIA_DB_CONFIG(user=None, password=None, dbname=None):
    return {
        "user": user if user is not None else os.getenv("MARIA_USER"),
        "password": password if password is not None else os.getenv("MARIA_PASSWORD"),
        "host": os.getenv("MARIA_HOST"),
        "port": int(os.getenv("MARIA_PORT")),
    }

MARIA_DB = MARIA_DB_CONFIG()
MARIA_AUTO_CONNECT = os.getenv('MARIA_AUTO_CONNECT', 'False').lower() == 'true'  # booléen