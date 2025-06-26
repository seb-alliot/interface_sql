def voir_contenu_table_postgres(table_name):
    """
    Retourne le contenu d'une table PostgreSQL.
    :param table_name: Nom de la table à consulter.
    :return: Requête SQL pour obtenir le contenu de la table.
    """
    # Nettoyer les guillemets doubles pour éviter erreurs ou injections
    safe_table_name = table_name.replace('"', '')
    return f'SELECT * FROM "{safe_table_name}";'