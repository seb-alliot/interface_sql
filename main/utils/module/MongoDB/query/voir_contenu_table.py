def voir_contenu_table(connection, choix_bdd, table_name):
    print("Type de table_name :", type(table_name))

    """
    Récupère tous les documents d'une collection MongoDB.

    Args:
        connection: Instance de connexion MongoDB (pymongo.MongoClient).
        choix_bdd: Nom de la base MongoDB à utiliser (str).
        table_name: Nom de la collection (str).

    Returns:
        Une liste de documents (list[dict]) ou [] en cas d'erreur.
    """

    connection = connection[0]
    if not connection or not choix_bdd or not table_name:
        return []

    if not isinstance(table_name, str):
        raise ValueError("Le nom de la collection doit être une liste de chaînes de caractères.")


    try:
        db = connection[choix_bdd]
        collection = db[table_name]
        documents = list(collection.find())
        if documents:
            return documents
        else:
            raise ValueError(f"La collection '{table_name}' est vide ou inexistante.")
    except Exception as e:
        raise Exception(f"Erreur lors de la récupération des documents : {e}")
