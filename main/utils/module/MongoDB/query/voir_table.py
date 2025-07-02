def voir_table(connection, choix_bdd):
    """
    Retourne la liste des collections (équivalent des tables) dans une base MongoDB donnée.
    """
    if not connection or not choix_bdd:
        return []
    try:
        db = connection[choix_bdd]
        return db.list_collection_names()
    except Exception as e:
        return []
