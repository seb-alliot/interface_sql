# main/utils/module/PostgreSQL/query/create.py
def create(connection, choix_bdd, table_name):
    """
    Crée une collection dans la base MongoDB spécifiée.
    Retourne True si la collection a été créée avec succès, False sinon.
    """
    connection = connection[0] if isinstance(connection, tuple) else connection
    if not connection or not choix_bdd or not table_name:
        return False
    try:
        db = connection[choix_bdd]
        db.create_collection(table_name)
        return True
    except Exception as e:
        print(f"Erreur MongoDB (create_collection) : {e}")
        return False
