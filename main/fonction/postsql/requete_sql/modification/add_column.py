import re

def is_valid_identifier(name):
    return bool(re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', name))

def column_exists(cursor, table_name, column_name):
    query = """
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.columns
            WHERE table_name=%s AND column_name=%s
        );
    """
    cursor.execute(query, (table_name, column_name))
    return cursor.fetchone()[0]

def modify_column(cursor, connection, table_name, column_name, new_column_type, default=None):
    if not (is_valid_identifier(table_name) and is_valid_identifier(column_name)):
        raise ValueError(f"Nom de table ou colonne invalide: {table_name}, {column_name}")

    try:
        if column_exists(cursor, table_name, column_name):
            # Changer le type
            query_type = f"ALTER TABLE {table_name} ALTER COLUMN {column_name} TYPE {new_column_type};"
            cursor.execute(query_type)

            # Mettre le DEFAULT si besoin
            if default is not None:
                if isinstance(default, str):
                    default_sql = f"'{default}'"
                else:
                    default_sql = str(default)
                query_default = f"ALTER TABLE {table_name} ALTER COLUMN {column_name} SET DEFAULT {default_sql};"
                cursor.execute(query_default)
            else:
                # Si default est None, on peut aussi supprimer l'ancien default
                query_drop_default = f"ALTER TABLE {table_name} ALTER COLUMN {column_name} DROP DEFAULT;"
                cursor.execute(query_drop_default)

            connection.commit()
            print(f"Colonne {column_name} modifiée dans la table {table_name}.")
        else:
            print(f"La colonne {column_name} n'existe pas dans la table {table_name}. Aucune action effectuée.")
    except Exception as e:
        print(f"Erreur lors de la modification de la colonne {column_name} : {e}")
        connection.rollback()
        raise e


def add_column(cursor, connection, table_name, column_name, column_type, default=None):
    if not (is_valid_identifier(table_name) and is_valid_identifier(column_name)):
        raise ValueError(f"Nom de table ou colonne invalide: {table_name}, {column_name}")

    try:
        if not column_exists(cursor, table_name, column_name):
            default_sql = ""
            if default is not None:
                if isinstance(default, str):
                    default_sql = f" DEFAULT '{default}'"
                else:
                    default_sql = f" DEFAULT {default}"

            query = f"ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS {column_name} {column_type}{default_sql};"
            cursor.execute(query)
            connection.commit()
            print(f"Colonne {column_name} ajoutée à la table {table_name}.")
        else:
            print(f"La colonne {column_name} existe déjà dans la table {table_name}. Aucune action effectuée.")
    except Exception as e:
        print(f"Erreur lors de l'ajout de la colonne {column_name} : {e}")
        connection.rollback()
        raise e
