def voir_table_postgres(table_name):
    # Nettoyer les guillemets doubles pour éviter erreurs ou injections
    safe_table_name = table_name.replace('"', '')
    return f'SELECT * FROM "{safe_table_name}";'
