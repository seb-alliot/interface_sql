

def table_name_exists(cursor, table_name):
    query = """
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_name=%s
        );
    """
    cursor.execute(query, (table_name,))
    return cursor.fetchone()[0]

def rename_table(cursor, connection, old_name, new_name):
    try:
        if table_name_exists(cursor, old_name):
            if not table_name_exists(cursor, new_name):
                query = f"ALTER TABLE {old_name} RENAME TO {new_name};"
                cursor.execute(query)
                connection.commit()
                print(f"Table {old_name} renommée en {new_name}.")
            else:
                print(f"Erreur : la table {new_name} existe déjà, renommage impossible.")
        else:
            print(f"Erreur : la table {old_name} n'existe pas, renommage impossible.")
    except Exception as e:
        print(f"Erreur lors du renommage de la table {old_name} : {e}")
        connection.rollback()
        raise e
