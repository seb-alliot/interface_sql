def voir_table_postgres():
    return "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public';"

