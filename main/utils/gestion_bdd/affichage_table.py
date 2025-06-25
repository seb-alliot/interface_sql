def recuperer_tables(style_base_donné, choix_bdd):
    from main.utils.module.maria_db import connect_to_maria_database, MARIA_DB_CONFIG
    from main.utils.module.postgres import connect_to_postgresql_database, POSTGRESQL_CONFIG
    from main.utils.module.mongo_db import connect_to_mongo, MONGO_DB_CONFIG
    from main.utils.fonction_diverse import Close

    if style_base_donné == "PostgreSQL":
        db_config = POSTGRESQL_CONFIG(dbname=choix_bdd)
        connection, error = connect_to_postgresql_database(db_config)
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public';")
                return [row[0] for row in cursor.fetchall()]
            finally:
                Close(connection, cursor)

    elif style_base_donné == "MariaDB":
        db_config = MARIA_DB_CONFIG(dbname=choix_bdd)
        connection, error = connect_to_maria_database(db_config)
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(f"SHOW TABLES FROM `{choix_bdd}`;")
                return [row[0] for row in cursor.fetchall()]
            finally:
                Close(connection, cursor)

    elif style_base_donné == "MongoDB":
        connection, error = connect_to_mongo(MONGO_DB_CONFIG())
        if connection:
            from main.utils.module.mongo_db.query.query_voir_base import voir_collections_mongo
            return voir_collections_mongo()
    return []
