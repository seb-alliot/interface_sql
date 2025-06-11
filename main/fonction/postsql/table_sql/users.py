import json

table_name = "USERS"

modele_structure = {
    "definition": {
        "columns": {
            "id": {
                "type": "SERIAL",
                "nullable": False,
                "default": None,
                "constraints": []
            },
            "username": {
                "type": "VARCHAR(100)",
                "nullable": False,
                "default": None,
                "constraints": ["UNIQUE"]
            },
            "email": {
                "type": "VARCHAR(255)",
                "nullable": False,
                "default": None,
                "constraints": ["UNIQUE"]
            },
            "password": {
                "type": "VARCHAR(255)",
                "nullable": False,
                "default": None,
                "constraints": []
            },
            "date_inscription": {
                "type": "TIMESTAMP",
                "nullable": False,
                "default": "CURRENT_TIMESTAMP",
                "constraints": []
            },
        },
        "primary_key": ["id"],
        "indexes": [
            {"columns": ["email"], "unique": True}
        ],
        "foreign_keys": [
            {
                "column": "role_id",
                "references": {
                    "table": "roles",
                    "column": "id"
                },
                "on_delete": "CASCADE",
                "on_update": "CASCADE"
            }
        ]
    }
}


structure_json = {
    "table_name": table_name,
    "definition": modele_structure["definition"]
}

json_string = json.dumps(structure_json, indent=4)

print(f"La table {table_name} en json_string:")
print(json_string)

with open("structure_users.json", "w") as f:
    f.write(json_string)
