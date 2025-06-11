from .verif_structure_bdd import verification_structure_bdd, normaliser_type_postgres

def comparer_defaults(modele_default, db_default):
    if modele_default is None and db_default is None:
        return True
    if isinstance(modele_default, (int, float)) and isinstance(db_default, str):
        try:
            return float(modele_default) == float(db_default)
        except ValueError:
            return False
    return str(modele_default) == str(db_default)

def comparer_types(modele_type, db_type, db_default):
    modele_type = modele_type.upper()
    db_type = db_type.upper()

    # --- Cas spécial SERIAL PostgreSQL ---
    if modele_type == "SERIAL":
        if db_type == "INTEGER":
            if db_default and isinstance(db_default, str) and "nextval(" in db_default.lower():
                return True
            return False
        return False

    # --- Cas VARCHAR(255) ≈ VARCHAR ---
    if modele_type.startswith("VARCHAR") and db_type.startswith("VARCHAR"):
        return True

    return modele_type == db_type


def comparaison(table_name, modele_structure, cursor):
    db_structure = verification_structure_bdd(table_name, cursor)

    if not db_structure:
        print(f"Aucune structure trouvée pour la table '{table_name}'.")
        return [{'action': 'create_table', 'table_name': table_name, 'structure': modele_structure}]

    differences = []

    modele_cols = set(modele_structure.keys())
    db_cols = set(db_structure.keys())

    # Colonnes à ajouter
    for col in modele_cols - db_cols:
        print(f"- Colonne '{col}' absente de la base.")
        differences.append({
            'action': 'ADD_column',
            'table': table_name,
            'column': col,
            'definition': modele_structure[col]
        })

    # Colonnes à supprimer
    for col in db_cols - modele_cols:
        print(f"- Colonne '{col}' est présente en base mais absente du modèle.")
        differences.append({
            'action': 'DROP_column',
            'table': table_name,
            'column': col,
            'definition': db_structure[col]
        })

    # Colonnes communes
    for col in modele_cols & db_cols:
        modele_def = modele_structure[col]
        db_def = db_structure[col]

        modele_type = normaliser_type_postgres(modele_def.get("type", ""))
        db_type = normaliser_type_postgres(db_def.get("type", ""))
        db_default = db_def.get("default")
        modele_default = modele_def.get("default")  # ✅ d'abord récupérer ici

        if not comparer_types(modele_type, db_type, db_default):
            print(f"- Colonne '{col}' a un type différent : modèle='{modele_type}', bdd='{db_type}'")
            differences.append({
                'action': 'MODIFY_column',
                'table': table_name,
                'column': col,
                'definition': modele_structure[col]
            })


        modele_nullable = modele_def.get("nullable", True)
        db_nullable = db_def.get("nullable", True)
        if modele_nullable != db_nullable:
            print(f"- Colonne '{col}' a une contrainte nullable différente : modèle={modele_nullable}, bdd={db_nullable}")
            differences.append({
                'action': 'MODIFY_column',
                'table': table_name,
                'column': col,
                'definition': modele_structure[col]
            })

    if differences:
        print(f"→ Des différences ont été détectées pour la table '{table_name}'.")
    else:
        print(f"✓ Aucun changement à effectuer pour '{table_name}'.")

    return differences
