from pymongo import MongoClient
from main.utils.module.mongo_db.connection import connect_to_mongo


def voir_collections_mongo(connection, choix_bdd):
    """
    Retourne la liste des collections dans une base MongoDB.
    """
    if not connection or not choix_bdd:
        return []

    try:
        db = connection[choix_bdd]
        return db.list_collection_names()
    except Exception as e:
        print(f"Erreur lors de la récupération des collections : {e}")
        return []
