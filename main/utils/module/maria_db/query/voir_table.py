def voir_table_maria(table_name):
    # On enlève les backticks dans le nom de table pour éviter les erreurs SQL ou injections
    safe_table_name = table_name.replace("`", "")
    return f"SELECT * FROM `{safe_table_name}`;"
