from main.utils.fonction_diverse import importer_module_bdd

def recuperer_tables(style_base_donne, connection, choix_bdd):
    module = importer_module_bdd(style_base_donne)
    if not connection:
        return ["Aucune connexion active"]

    # Pour MongoDB, pas de cursor, on appelle direct la fonction spécifique
    if style_base_donne == "MongoDB":
        try:
            query_module = module.import_query_module("voir_table")
            table_names = query_module.voir_table(style_base_donne, connection, choix_bdd)
            if not table_names:
                return f"Aucune table trouvé"
            else:
                return table_names
        except Exception as e:
            return [f"Erreur lors de la récupération des collections : {str(e)}"]

    # Pour SQL (PostgreSQL, MariaDB), on crée un cursor et exécute la requête
    connection = connection[0]
    if not connection:
        return ["Connexion invalide"]

    cursor = connection.cursor()
    query_module = module.import_query_module("voir_table")

    query = None
    if style_base_donne == "PostgreSQL":
        query = query_module.voir_table()
    elif style_base_donne == "MariaDB":
        query = query_module.voir_table(choix_bdd)

    if query is not None:
        try:
            cursor.execute(query)
            print(f"Requête SQL exécutée : {query}")
            table_names = [row[0] for row in cursor.fetchall()]
            return table_names
        except Exception as e:
            return [f"Erreur lors de la récupération des tables : {str(e)}"]

    return []
