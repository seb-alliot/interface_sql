def name_exists(cursor, table_name, column_name):
    query = """
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.columns
            WHERE table_name=%s AND column_name=%s
        );
    """
    cursor.execute(query, (table_name, column_name))
    return cursor.fetchone()[0]

def rename_column(cursor, connection, table_name, old_name, new_name):
    try:
        if name_exists(cursor, table_name, old_name):
            query = f"ALTER TABLE {table_name} RENAME COLUMN {old_name} TO {new_name};"
            cursor.execute(query)
            connection.commit()
            print(f"Colonne {old_name} renommée en {new_name} dans la table {table_name}.")
        else:
            print(f"La colonne {old_name} n'existe pas dans la table {table_name}. Aucun renommage effectué.")
    except Exception as e:
        print(f"Erreur lors du renommage de la colonne {old_name} : {e}")
        connection.rollback()
        raise e
