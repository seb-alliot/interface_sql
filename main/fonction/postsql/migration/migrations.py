# === IMPORTS & CONFIGURATION DU CONTEXTE D'EXÉCUTION ===
import sys, os, importlib
from .connection_db import connect_to_database
from .comparaison import comparaison
from .applique_modifications import applique_modifications
from ..requete_sql.creation.create_table import creer_table
from ..historique.code import logique_log
log_and_print = logique_log.log_and_print


# Détection du chemin racine du projet et ajout au sys.path si nécessaire
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# === FONCTION PRINCIPALE DE MIGRATION ===
def Migrations():
    log_and_print("Starting migration...")
    connection = None
    cursor = None
    try:
        connection, cursor = connect_to_database()
        log_and_print("Connexion à la base de données...")

        base_path = os.path.dirname(os.path.abspath(__file__))
        classe_sql_path = os.path.abspath(os.path.join(base_path, 'classe_sql'))

        for filename in os.listdir(classe_sql_path):
            if filename.endswith('.py') and filename != '__init__.py':
                log_and_print(f"Traitement du fichier: {filename}")
                module_name = filename[:-3]

                try:
                    module = importlib.import_module(f'app.backend.migrations.classe_sql.{module_name}')
                    log_and_print(f"Module {module_name} importé avec succès.")

                    modele_structure = getattr(module, 'modele_structure', None)
                    table_name = getattr(module, 'table_name', None)

                    if modele_structure and table_name:
                        columns_modele = modele_structure.get("definition", {}).get("columns", {})

                        differences = comparaison(table_name, columns_modele, cursor)

                        if differences:
                            if isinstance(differences[0], dict) and differences[0].get('action') == 'create_table':
                                # Passer la structure complète ici à la création
                                log_and_print(f"Table {table_name} absente en BDD, création automatique...")
                                entre_une_reponse = input("Créer la table ? [Y/n]: ").strip().lower()
                                if entre_une_reponse in ('y', 'yes'):
                                    creer_table(cursor, connection, modele_structure, table_name)

                                else:
                                    log_and_print("Création de la table annulée.")
                            else:
                                entre_une_reponse = input("Appliquer les modifications ? [Y/n]: ").strip().lower()
                                if entre_une_reponse in ('y', 'yes', ''):
                                    changement_effectue = applique_modifications(cursor, connection, differences)
                                    log_and_print("Modifications appliquées avec succès.")
                                else:
                                    log_and_print("Aucune modification appliquée.")
                        else:
                            log_and_print(f"Aucune modification nécessaire pour la table {table_name}.")

                except ImportError as e:
                    log_and_print(f"Erreur lors de l'import du module {module_name}: {e}")
                    if connection:
                        connection.rollback()

    except Exception as e:
        log_and_print(f"Erreur globale pendant la migration : {e}")

    finally:
        if connection:
            connection.commit()
        if cursor:
            cursor.close()
        if connection:
            connection.close()
# === POINT D'ENTRÉE DU SCRIPT ===
if __name__ == "__main__":
    Migrations()