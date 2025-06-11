def modify_column(cursor, connection, table_name, column_name, column_type=None, default_value=None, nullable=None):
    try:
        if column_type:
            cursor.execute(f'ALTER TABLE "{table_name}" ALTER COLUMN "{column_name}" TYPE {column_type};')
        if default_value is not None:
            if isinstance(default_value, str) and not default_value.upper().startswith(("CURRENT_TIMESTAMP", "NULL")):
                default_sql = f"'{default_value}'"
            else:
                default_sql = default_value
            cursor.execute(f'ALTER TABLE "{table_name}" ALTER COLUMN "{column_name}" SET DEFAULT {default_sql};')
        else:
            cursor.execute(f'ALTER TABLE "{table_name}" ALTER COLUMN "{column_name}" DROP DEFAULT;')

        if nullable is not None:
            if not nullable:
                cursor.execute(f'ALTER TABLE "{table_name}" ALTER COLUMN "{column_name}" SET NOT NULL;')
            else:
                cursor.execute(f'ALTER TABLE "{table_name}" ALTER COLUMN "{column_name}" DROP NOT NULL;')

        connection.commit()
        print(f"Colonne {column_name} modifiée dans la table {table_name}.")
    except Exception as e:
        print(f"Erreur modification colonne {column_name} : {e}")
        connection.rollback()
