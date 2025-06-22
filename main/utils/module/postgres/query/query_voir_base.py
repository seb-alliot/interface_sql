def voir_base_postgresql():
    return "SELECT datname FROM pg_database WHERE datistemplate = false;"
