# main/utils/module/PostgreSQL/query/create.py

def create(table_name):
    def builder(*colonnes):
        champs = ", ".join([col for col in colonnes if col])
        return f' CREATE TABLE "{table_name}" ({champs}); '
    return builder
