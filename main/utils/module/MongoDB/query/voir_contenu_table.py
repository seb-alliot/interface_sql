def voir_contenu_table(connection, choix_bdd, table_name):
    """
    Récupère tous les documents d'une collection MongoDB.

    Args:
        connection: Instance de connexion MongoDB (pymongo.MongoClient).
        choix_bdd: Nom de la base MongoDB à utiliser (str).
        table_name: Nom de la collection (str).

    Returns:
        Une liste de documents (list[dict]) ou [] en cas d'erreur.
    """
    if not connection or not choix_bdd or not table_name:
        print("❌ Paramètre manquant pour la lecture MongoDB.")
        return []

    if not isinstance(table_name, str):
        raise ValueError("Le nom de la collection doit être une chaîne de caractères.")

    try:
        db = connection[choix_bdd]
        collection = db[table_name]
        documents = list(collection.find())
        print(f"✅ {len(documents)} documents lus depuis {choix_bdd}.{table_name}")
        return documents
    except Exception as e:
        print(f"❌ Erreur lors de la lecture MongoDB : {e}")
        return []
