def voir_table():
    return "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public';"
