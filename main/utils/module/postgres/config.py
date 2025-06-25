import os

def POSTGRESQL_CONFIG(user=None, password=None, dbname=None):
    return {
        "dbname": dbname if dbname is not None else os.getenv("POSTGRESQL_NAME"),
        "user": user if user is not None else os.getenv("POSTGRESQL_USER"),
        "password": password if password is not None else os.getenv("POSTGRESQL_PASSWORD"),
        "host": os.getenv("POSTGRESQL_HOST"),
        "port": int(os.getenv("POSTGRESQL_PORT", 5432)),
    }

POSTGRES_DB = POSTGRESQL_CONFIG()
# On convertis la variable d'environnement en booléen, car un str n'est pas un booléen mais une chaîne de caractères
# on fait donc une comparaison pour renvoyer tru ou false
POSTGRESQL_AUTO_CONNECT = os.getenv('POSTGRESQL_AUTO_CONNECT', 'False').lower() == 'true'  # booléen

def postgresql_auto_connect():
    return os.getenv('POSTGRESQL_AUTO_CONNECT', 'False').lower() == 'true'
