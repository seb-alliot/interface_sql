# test_create_table_modules.py

import sys
from pathlib import Path

# Ajoute le dossier racine à sys.path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from main.utils.fonction_diverse.import_modul import importer_module_bdd


def importer_modules_sgbd(style_base_donne):
    module_bdd = importer_module_bdd(style_base_donne)

    modules = {
        "create": module_bdd.import_query_module("create"),
    }

    # MongoDB n'a pas besoin des autres modules
    if style_base_donne.lower() != "mongodb":
        modules.update({
            "choix_id": module_bdd.import_query_module("choix_id"),
            "contrainte": module_bdd.import_query_module("contrainte"),
            "clef_primaire": module_bdd.import_query_module("clef_primaire"),
        })

    return modules


def tester_creation_table(style_base_donne, table_name, type_id=None, contrainte_val=None, valeur_default=None, clef_primaire=None):
    print(f"\n🧪 Test SGBD : {style_base_donne}")
    modules = importer_modules_sgbd(style_base_donne)

    if style_base_donne.lower() == "mongodb":
        # MongoDB ne construit pas de requête SQL, on simule la création
        create_func = modules["create"].create
        connection_fake = {"testdb": {}}  # connexion fictive pour le test
        choix_bdd = "testdb"
        result = create_func(connection_fake, choix_bdd, table_name)
        print(f"📦 Collection MongoDB créée (simulé) : {table_name} -> {result}")
        return

    # Traitement SGBD classiques
    type_colonne = modules["choix_id"].choix_id(type_id)

    if contrainte_val == "DEFAULT":
        if valeur_default is None:
            raise ValueError("Il faut une valeur par défaut pour DEFAULT.")
        contrainte_sql = f"DEFAULT '{valeur_default}'"
    else:
        contrainte_sql = modules["contrainte"].contrainte(contrainte_val)

    clef_sql = modules["clef_primaire"].clef_primaire(clef_primaire)

    colonne = f"id {type_colonne}"
    if contrainte_sql:
        colonne += f" {contrainte_sql}"
    if clef_sql:
        colonne += f" {clef_sql}"

    requete = modules["create"].create(table_name)(colonne)
    print(f"🔧 Requête générée :\n{requete}")


if __name__ == "__main__":
    tester_creation_table(
        style_base_donne="PostgreSQL",
        table_name="utilisateur",
        type_id="SERIAL",
        contrainte_val="Aucune",
        clef_primaire="PRIMARY KEY"
    )

    tester_creation_table(
        style_base_donne="MariaDB",
        table_name="client",
        type_id="INT",
        contrainte_val="DEFAULT",
        valeur_default="1",
        clef_primaire="PRIMARY KEY"
    )

    tester_creation_table(
        style_base_donne="MongoDB",
        table_name="commande"
    )
