def voir_base(connection):
    return connection.list_database_names() if connection else ["Aucune connexion active"]
