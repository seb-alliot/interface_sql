import os
import sys
import importlib
from ..historique.code import logique_log
log_and_print = logique_log.log_and_print
from ..requete_sql.modification import modifier_column


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

def split_type_and_default(parts):
    # Recherche 'DEFAULT' dans la liste
    if "DEFAULT" in parts:
        index = parts.index("DEFAULT")
        column_type = " ".join(parts[:index])
        default_value = " ".join(parts[index+1:])
        return column_type, default_value
    else:
        return " ".join(parts), None

def applique_modifications(cursor, connection, differences, definition):
    changements_effectues = []
    modif_pkg = 'app.backend.migrations.fonction_sql.modif'
    delete_pkg = 'app.backend.migrations.fonction_sql.delete'
    create_pkg = 'app.backend.migrations.fonction_sql.create'

    for diff in differences:
        parts = diff.strip().split()
        if not parts:
            continue

        action = parts[0].upper()

        try:
            if action == "ADD":
                table_name = parts[1]
                column_name = parts[2]
                column_type, default_value = split_type_and_default(parts[3:])
                module = importlib.import_module(f'{modif_pkg}.add_column')
                module.add_column(cursor, connection, table_name, column_name, column_type, default_value)
                changements_effectues.append(f"Ajout de la colonne {column_name} dans la table {table_name}")
                log_and_print(f"Ajout de la colonne {column_name} dans la table {table_name}")

            elif action == "MODIFY":
                table_name = parts[1]
                column_name = parts[2]
                raw_definition = parts[3:]

                column_type, default_value = split_type_and_default(raw_definition)
                module.modify_column(cursor, connection, table_name, column_name)

                # Charger le bon module (tu peux garder ton système si tu veux le modulariser)
                modify_column(cursor, connection, table_name, column_name, column_type, default_value)

                changements_effectues.append(f"Modification de la colonne {column_name} dans la table {table_name}")
                log_and_print(f"Modification de la colonne {column_name} dans la table {table_name}")

            elif action == "DROP":
                table_name = parts[1]
                column_name = parts[2]
                module = importlib.import_module(f'{modif_pkg}.delete_column')
                module.delete_column(cursor, connection, table_name, column_name)
                changements_effectues.append(f"Suppression de la colonne {column_name} dans la table {table_name}")
                log_and_print(f"Suppression de la colonne {column_name} dans la table {table_name}")

            elif action == "DELETE":
                table_name = parts[1]
                module = importlib.import_module(f'{delete_pkg}.delete_table')
                module.delete_table(cursor, connection, table_name)
                changements_effectues.append(f"Suppression de la table {table_name}")
                log_and_print(f"Suppression de la table {table_name}")

            elif action == "RENAME":
                old_name = parts[1]
                new_name = parts[2]
                module = importlib.import_module(f'{modif_pkg}.rename_table')
                module.rename_table(cursor, connection, old_name, new_name)
                changements_effectues.append(f"Renommage de la table {old_name} en {new_name}")
                log_and_print(f"Renommage de la table {old_name} en {new_name}")

            elif action == "RENAME_COLUMN":
                table_name = parts[1]
                old_column_name = parts[2]
                new_column_name = parts[3]
                module = importlib.import_module(f'{modif_pkg}.rename_column')
                module.rename_column(cursor, connection, table_name, old_column_name, new_column_name)
                changements_effectues.append(f"Renommage de la colonne {old_column_name} en {new_column_name} dans la table {table_name}")
                log_and_print(f"Renommage de la colonne {old_column_name} en {new_column_name} dans la table {table_name}")

            elif action == "CREATE":
                table_name = parts[1]
                module = importlib.import_module(f'{create_pkg}.create_table')
                module.create_table(cursor, connection, table_name, definition)
                changements_effectues.append(f"Création de la table {table_name}")
                log_and_print(f"Création de la table {table_name}")

            else:
                log_and_print(f"Instruction inconnue ou non prise en charge : {diff}")

        except Exception as e:
            log_and_print(f"Erreur lors de l'exécution de '{diff}': {e}")
            connection.rollback()
        if connection:
            connection.commit()
    return changements_effectues