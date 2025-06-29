import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
load_dotenv()

def MONGO_DB_CONFIG():
    return {
        "user": os.getenv("MONGO_USER"),
        "password": os.getenv("MONGO_PASSWORD"),
        "host": os.getenv("MONGO_HOST"),
        "database": os.getenv("MONGO_NAME"),  # nom de la base
        "app_name": os.getenv("MONGO_NAME", "Cluster0"),
    }

def connect(config=None):
    if config is None or callable(config):
        config = MONGO_DB_CONFIG()

    user = config.get("user")
    password = config.get("password")
    host = config.get("host")
    dbname = config.get("database")
    app_name = config.get("app_name", "Cluster0")

    if not all([user, password, host, dbname]):
        return None, "Configuration MongoDB incomplète"

    uri = f"mongodb+srv://{user}:{password}@{host}/?retryWrites=true&w=majority&appName={app_name}"

    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        return client, None
    except ConnectionFailure as e:
        return None, f"ConnectionFailure: {str(e)}"
    except Exception as e:
        return None, f"Erreur inattendue: {str(e)}"


if __name__ == "__main__":
    config = MONGO_DB_CONFIG()

    print("🔧 Test de la configuration MongoDB :")
    print(f"Database     : {config.get('database')}")
    print(f"User         : {config.get('user')}")
    print(f"Host         : {config.get('host')}")
    # port n'existe pas ici, donc on l'enlève
    print(f"Auto Connect : {os.getenv('MONGO_AUTO_CONNECT')}")

    # Reconstruire l'URI pour affichage
    uri = f"mongodb+srv://{config.get('user')}:{config.get('password')}@{config.get('host')}/?retryWrites=true&w=majority&appName={config.get('app_name')}"
    print(f"URI          : {uri.replace(config.get('password'), '***')}")

    print("\n🔌 Tentative de connexion à MongoDB...")
    client, error = connect(config)
    if client:
        print("✅ Connexion à MongoDB réussie !")
        print("📁 Bases disponibles :", client.list_database_names())
    else:
        print(f"❌ Échec de la connexion : {error}")