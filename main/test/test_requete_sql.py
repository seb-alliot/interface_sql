# Simulation des modules importés et fonctions utilisées

def create(table_name):
    def builder(*colonnes):
        champs = ", ".join([col for col in colonnes if col])
        # Correction de la syntaxe SQL : nom de table non entre guillemets mais sans espaces
        return f"CREATE TABLE {table_name} ({champs});"
    return builder

def choix_id(type_id):
    # Ici on simule juste la valeur retournée telle quelle, sauf pour SERIAL/BIGSERIAL où c'est spécial
    if type_id in ["SERIAL", "BIGSERIAL"]:
        return type_id
    return type_id

def clef_primaire(clef):
    if clef == "PRIMARY KEY":
        return "PRIMARY KEY"
    return ""

def contrainte(contraint):
    if contraint == "NOT NULL":
        return "NOT NULL"
    elif contraint == "UNIQUE":
        return "UNIQUE"
    elif contraint == "DEFAULT":
        # Géré à part car valeur par défaut nécessaire
        return "DEFAULT"
    elif contraint == "CHECK":
        return "CHECK (id > 0)"
    return ""

# Listes des choix possibles
types_id = ["INT", "BIGINT", "SMALLINT", "VARCHAR", "TEXT", "DATE", "TIMESTAMP", "SERIAL", "BIGSERIAL"]
contraintes = ["Aucune", "NOT NULL", "UNIQUE", "DEFAULT", "CHECK"]
clefs = ["Aucune", "PRIMARY KEY"]

# Fonction simple pour vérifier si combinaison est valide (ex: pas DEFAULT avec SERIAL)
def est_valide(type_id, contrainte, clef):
    if type_id in ["SERIAL", "BIGSERIAL"]:
        # SERIAL et BIGSERIAL ne peuvent pas avoir de contrainte DEFAULT
        if contrainte == "DEFAULT":
            return False
    # Ex: PRIMARY KEY nécessite NOT NULL ou est NOT NULL implicite (on accepte ici)
    # On peut étendre ici si besoin
    return True

# Génération des requêtes pour toutes combinaisons valides
for type_id in types_id:
    for contrainte in contraintes:
        for clef in clefs:
            if not est_valide(type_id, contrainte, clef):
                continue

            table_name = "ma_table"
            query_name = create(table_name)

            type_colonne = choix_id(type_id)

            definition_colonne = f"id {type_colonne}"

            if contrainte == "DEFAULT":
                default_value = "'42'"  # valeur par défaut fictive pour test
                definition_colonne += f" DEFAULT {default_value}"
            elif contrainte != "Aucune":
                definition_colonne += f" {contrainte}"

            if clef != "Aucune":
                definition_colonne += f" {clef_primaire(clef)}"

            requete = query_name(definition_colonne)

            print(f"Requête générée : {requete}")
