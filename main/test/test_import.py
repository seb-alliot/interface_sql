# Importer la fonction d'import dynamique de modules BDD
from ..utils.fonction_diverse.import_modul import importer_module_bdd
import os
from dotenv import load_dotenv

load_dotenv()

print("DB_USER:", os.getenv("DB_USER"))
print("DB_PASSWORD:", os.getenv("DB_PASSWORD"))
print("DB_HOST:", os.getenv("DB_HOST"))
print("DB_PORT:", os.getenv("DB_PORT"))
print("DB_NAME:", os.getenv("DB_NAME"))

def test_module_bdd(style_base_donne):
    print(f"=== Test pour la base : {style_base_donne} ===")

    try:
        # Importer la classe ModuleBDD et les modules config+connection
        module_bdd = importer_module_bdd(style_base_donne)

        # Récupérer la config (avec ou sans paramètres)
        config = module_bdd.config()  # Ou module_bdd.config(dbname='test_db')

        print("Config obtenue :", config)

        # Se connecter à la base
        connexion, erreur = module_bdd.connect(config)
        if erreur:
            print("Erreur de connexion :", erreur)
            return
        print("Connexion OK :", connexion)

        # Importer dynamiquement un module de requête, par exemple 'voir_base'
        query_module = module_bdd.import_query_module("voir_base")
        if not query_module:
            print("Module query 'voir_base' non trouvé")
            return

        # Appeler une fonction du module query (par exemple 'lister_bases')
        # Remplace par la fonction réelle définie dans voir_base.py
        bases = query_module.voir_base(connexion)
        print("Bases listées :", bases)

    except ImportError as e:
        print("Erreur d'importation :", e)
    except Exception as ex:
        print("Erreur inattendue :", ex)

if __name__ == "__main__":
    # Lancer le test avec une base existante (PostgreSQL, MariaDB, MongoDB)
    test_module_bdd("PostgreSQL")
