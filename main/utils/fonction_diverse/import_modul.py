import importlib

class ModuleBDD:
    def __init__(self, config_module, connection_module):
        self._config_module = config_module
        self._connection_module = connection_module

    def config(self, **kwargs):
        return self._config_module.config(**kwargs)

    def connect(self, db_config=None):
        return self._connection_module.connect(db_config)

    def auto_connect(self):
        return self._config_module.auto_connect()

    def import_query_module(self, query_name):
        """
        Importe dynamiquement un module query, ex : voir_base, voir_table...
        """
        try:
            # Exemple : main.utils.module.PostgreSQL.config → on garde jusqu’à PostgreSQL
            base_path = '.'.join(self._config_module.__name__.split('.')[:-1])
            module_path = f"{base_path}.query.{query_name}"
            module_query = importlib.import_module(module_path)
            print(f"✅ Module query importé : {module_path}")
            return module_query
        except ModuleNotFoundError as e:
            print(f"❌ Module query '{query_name}' non trouvé dans {base_path} : {e}")
            return None

def importer_module_bdd(style_base_donné):
    base_path = f"main.utils.module.{style_base_donné}"

    try:
        module_config = importlib.import_module(f"{base_path}.config")
        module_connection = importlib.import_module(f"{base_path}.connection")
        return ModuleBDD(module_config, module_connection)
    except ModuleNotFoundError as e:
        raise ImportError(f"Erreur d'importation dans {style_base_donné} : {e}")
