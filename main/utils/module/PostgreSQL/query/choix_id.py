def choix_id(type_id):
    if type_id and type_id != " Aucune ":
        return f" {type_id} "
    else:
        return ""