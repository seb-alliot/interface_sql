# Permet d'importer dynamiquement un module Python à partir d'une chaîne
import importlib

class ModuleBDD:
    """
    Cette classe encapsule les modules de configuration et de connexion
    pour un type de base de données donné (PostgreSQL, MariaDB, MongoDB...).
    Elle permet aussi d'importer dynamiquement des modules de requêtes (ex: voir_base).
    """

    def __init__(self, config_module, connection_module):
        """
        Initialise un objet ModuleBDD avec deux modules :
        - config_module : module contenant les fonctions de configuration
        - connection_module : module contenant la fonction de connexion
        """
        self._config_module = config_module
        self._connection_module = connection_module

    def config(self, **kwargs):
        """
        Appelle la fonction config() du module de configuration.
        Elle retourne un dictionnaire avec les paramètres de connexion (host, user, dbname, etc.).
        Les paramètres peuvent être passés dynamiquement.
        """
        return self._config_module.config(**kwargs)

    def connect(self, db_config=None):
        """
        Appelle la fonction connect() du module de connexion.
        Cette fonction retourne généralement un tuple : (connexion, message)
        """
        return self._connection_module.connect(db_config)

    def auto_connect(self):
        """
        Appelle auto_connect() du module de configuration.
        Cette méthode permet une connexion automatique avec des valeurs par défaut (souvent depuis un fichier .env).
        """
        return self._config_module.auto_connect()

    def import_query_module(self, query_name):
        """
        Importe dynamiquement un module Python contenant des requêtes spécifiques.
        Exemple :
            Si query_name = 'voir_base'
            Et _config_module.__name__ = 'main.utils.module.PostgreSQL.config'
            Alors on importe : 'main.utils.module.PostgreSQL.query.voir_base'
        """
        try:
            # Exemple : 'main.utils.module.PostgreSQL.config' → ['main', 'utils', 'module', 'PostgreSQL']
            base_path = '.'.join(self._config_module.__name__.split('.')[:-1])

            # Ajoute 'query.query_name' pour créer le chemin complet du module
            module_path = f"{base_path}.query.{query_name}"

            # Importation dynamique du module ciblé
            module_query = importlib.import_module(module_path)

            # Affiche dans la console le module qui a été chargé
            print(f"✅ Module query importé : {module_path}")

            # Retourne le module prêt à être utilisé
            return module_query

        except ModuleNotFoundError as e:
            # Si le module n'existe pas, on affiche une erreur et retourne None
            print(f"❌ Module query '{query_name}' non trouvé dans {base_path} : {e}")
            return None


def importer_module_bdd(style_base_donné):
    """
    Fonction externe qui permet d'importer tous les modules nécessaires à une BDD spécifique.
    Elle retourne un objet ModuleBDD contenant :
    - Le module de configuration
    - Le module de connexion

    Exemple :
        importer_module_bdd("PostgreSQL")
        → importe main.utils.module.PostgreSQL.config
        → importe main.utils.module.PostgreSQL.connection
    """

    # Construit la base du chemin des modules à importer
    base_path = f"main.utils.module.{style_base_donné}"

    try:
        # Importe le module de configuration (config.py)
        module_config = importlib.import_module(f"{base_path}.config")

        # Importe le module de connexion (connection.py)
        module_connection = importlib.import_module(f"{base_path}.connection")

        # Retourne une instance de ModuleBDD avec les deux modules
        return ModuleBDD(module_config, module_connection)

    except ModuleNotFoundError as e:
        # Si un des deux modules est manquant, on lève une erreur explicite
        raise ImportError(f"Erreur d'importation dans {style_base_donné} : {e}")

