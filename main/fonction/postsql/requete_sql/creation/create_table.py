def creer_table(cursor, connection, modele_structure, table_name):
    colonnes = []
    colonnes_def = modele_structure.get("definition", {}).get("columns", {})
    clef_primaire = modele_structure.get("definition", {}).get("primary_key", [])

    for colonne_name, colonne_proprietes in colonnes_def.items():
        colonne_type = colonne_proprietes.get("type", "TEXT")
        nullable = colonne_proprietes.get("nullable", True)
        default = colonne_proprietes.get("default", None)
        constraints = colonne_proprietes.get("constraints", [])

        colonne_sql = f'"{colonne_name}" {colonne_type}'
        if not nullable:
            colonne_sql += " NOT NULL"

        if colonne_type.upper() != "SERIAL" and default is not None:
            if isinstance(default, str) and not default.upper().startswith(("CURRENT_TIMESTAMP", "NULL")) and "nextval(" not in default.lower():
                colonne_sql += f" DEFAULT '{default}'"
            else:
                colonne_sql += f" DEFAULT {default}"

        for constraint in constraints:
            if constraint.upper() == "UNIQUE":
                colonne_sql += " UNIQUE"
            elif constraint.upper().startswith("CHECK"):
                colonne_sql += f" {constraint}"

        colonnes.append(colonne_sql)

    if clef_primaire:
        colonnes.append(f"PRIMARY KEY ({', '.join(f'\"{col}\"' for col in clef_primaire)})")

    colonnes_sql = ", ".join(colonnes)
    requete = f'CREATE TABLE IF NOT EXISTS "{table_name}" ({colonnes_sql});'

    # --- Exécution de la requête ---
    cursor.execute(requete)
    connection.commit()

    print(f"Table '{table_name}' créée avec succès.")

    return requete  # je la retourne pour vérification ou log si besoin
