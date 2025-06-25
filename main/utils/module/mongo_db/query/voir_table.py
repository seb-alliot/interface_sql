def voir_contenu_collection_mongo(connection_mongo, choix_bdd, table_name):
    """
    Récupère tous les documents d'une collection MongoDB.
    """
    if not connection_mongo or not choix_bdd or not table_name:
        return []

    if not isinstance(table_name, str):
        raise ValueError("Le nom de la collection doit être une chaîne de caractères.")

    try:
        db = connection_mongo[choix_bdd]
        collection = db[table_name]
        if not collection:

            return f"La collection '{table_name}' n'existe pas dans la base de données '{choix_bdd}'."
        return list(collection.find())
    except Exception as e:
        print(f"Erreur lors de la récupération de la collection : {e}")
        return []
