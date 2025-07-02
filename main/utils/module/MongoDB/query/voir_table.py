def voir_table(style_base_donne, connection, choix_bdd):
    """
    Retourne la liste des collections (équivalent des tables) dans une base MongoDB donnée.
    """
    print(f"Récupération des collections pour la base {choix_bdd} dans le style {style_base_donne}")
    connection = connection[0] if isinstance(connection, tuple) else connection
    if not connection or not choix_bdd:
        return []
    try:
        db = connection[choix_bdd]
        return db.list_collection_names()
    except Exception as e:
        print(f"Erreur lors de la récupération des collections : {e}")
        return []
