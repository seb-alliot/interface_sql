import os
import sys
import keyring
from dotenv import load_dotenv

# Chemin du dossier de l'exécutable (ou script en dev)
base_path = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
load_dotenv(dotenv_path=os.path.join(base_path, '.env'))

APP_SECRET = os.getenv('APP_SECRET')
APP_NAME = "Interface SQL - By Itsuki"
VERSION = os.getenv("APP_VERSION", "0.0")
DB_AUTO_CONNECT = os.getenv('DB_AUTO_CONNECT', 'False').lower() == 'true'


# Service name utilisé dans keyring pour stocker les infos BDD
KEYRING_SERVICE = f"{APP_NAME}"

def MAJ_DB_CONFIG(user=None, password=None):
    """
    Retourne la config BDD avec user/pass potentiellement fournis à la main,
    le reste est récupéré via keyring.
    """
    return {
        'dbname': keyring.get_password(KEYRING_SERVICE, 'DBNAME'),
        'user': user if user is not None else keyring.get_password(KEYRING_SERVICE, 'USER'),
        'password': password if password is not None else keyring.get_password(KEYRING_SERVICE, 'PASSWORD'),
        'host': keyring.get_password(KEYRING_SERVICE, 'HOST'),
        'port': keyring.get_password(KEYRING_SERVICE, 'PORT') or '5432',
    }
# Optionnel : version instantanée au lancement
DB_CONFIG = MAJ_DB_CONFIG()
