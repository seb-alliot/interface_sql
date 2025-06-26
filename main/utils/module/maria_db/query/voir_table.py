def voir_table_maria(nom_base):
    # retourne une requête pour lister les tables d’une base spécifique
    return f"SHOW TABLES FROM `{nom_base}`;"