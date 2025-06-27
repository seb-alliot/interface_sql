def recuperer_tables(style_base_donné,connection, choix_bdd):
    from main.utils.module.maria_db import  voir_table_maria
    from main.utils.module.postgres import voir_table_postgres
    from main.utils.module.mongo_db import voir_collections_mongo
    connection = connection

    if style_base_donné == "PostgreSQL":
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(voir_table_postgres())
                table_names= [row[0] for row in cursor.fetchall()]
                return table_names
            except Exception as e:
                return [f"Erreur lors de la récupération des tables : {str(e)}"]

    elif style_base_donné == "MariaDB":
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(voir_table_maria(choix_bdd))
                table_names = cursor.fetchall()
                return [row[0] for row in cursor.fetchall()]
            except Exception as e:
                return [f"Erreur lors de la récupération des tables : {str(e)}"]

    elif style_base_donné == "MongoDB":
        if connection:
            table_names = voir_collections_mongo(connection, choix_bdd)
            return table_names

    return []
