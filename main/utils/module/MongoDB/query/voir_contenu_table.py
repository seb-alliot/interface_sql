def voir_contenu_table(connection, choix_bdd, table_name):
    """
    Récupère tous les documents d'une collection MongoDB.
    """
    if not connection or not choix_bdd or not table_name:
        return []

    if not isinstance(table_name, str):
        raise ValueError("Le nom de la collection doit être une chaîne de caractères.")

    try:
        db = connection[choix_bdd]
        collection = db[table_name]
        return list(collection.find())
    except Exception as e:
        return []