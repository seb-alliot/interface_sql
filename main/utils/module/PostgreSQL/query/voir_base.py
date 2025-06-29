def voir_base():
    return "SELECT datname FROM pg_database WHERE datistemplate = false;"
