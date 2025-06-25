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


