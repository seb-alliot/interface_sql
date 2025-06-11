import json
import re


def normaliser_type_postgres(type_pg):
    """
    Simplifie les types PostgreSQL vers des types standards pour comparaison.
    Ignore les tailles et gère les alias comme SERIAL -> INTEGER.
    """
    if not type_pg:
        return None

    # Nettoyage du type (ex : VARCHAR(100) → VARCHAR)
    type_pg = type_pg.lower()
    type_pg = re.sub(r'\(.*?\)', '', type_pg)  # retire (255), (100)...
    type_pg = type_pg.strip()

    # Correspondances standards
    if "character varying" in type_pg or "varchar" in type_pg:
        return "VARCHAR"
    elif "character" in type_pg or "char" in type_pg:
        return "CHAR"
    elif "serial" in type_pg:
        return "INTEGER"  # PostgreSQL transforme SERIAL en INTEGER + sequence
    elif "timestamp" in type_pg:
        return "TIMESTAMP"
    elif "integer" in type_pg or "int" in type_pg:
        return "INTEGER"
    elif "boolean" in type_pg:
        return "BOOLEAN"
    elif "double precision" in type_pg or "float8" in type_pg:
        return "FLOAT"
    elif "numeric" in type_pg or "decimal" in type_pg:
        return "DECIMAL"
    elif "text" in type_pg:
        return "TEXT"
    elif "date" in type_pg:
        return "DATE"

    return type_pg.upper()

def verification_structure_bdd(table_name, cursor):
    # Récupérer les colonnes
    cursor.execute("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_name = %s;
    """, (table_name,))

    colonnes = cursor.fetchall()
    structure = {}

    for nom_colonne, data_type, is_nullable, column_default in colonnes:
        type_normalise = normaliser_type_postgres(data_type)

        structure[nom_colonne] = {
            "type": type_normalise,
            "nullable": (is_nullable == 'YES'),
            "default": column_default,
            "constraints": []
        }

    # Optionnel : récupérer la clé primaire
    cursor.execute("""
        SELECT kcu.column_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu
        ON tc.constraint_name = kcu.constraint_name
        AND tc.table_name = kcu.table_name
        WHERE tc.table_name = %s AND tc.constraint_type = 'PRIMARY KEY';
    """, (table_name,))
    pk_cols = [row[0] for row in cursor.fetchall()]


    print(f"Structure de la table '{table_name}': {json.dumps(structure, indent=2)}")
    return structure
