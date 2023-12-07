from settings import database, sql_provider


def cargo_info_by_name(cargo_name: str):
    with database as cursor:
        if cursor:
            sql_code = sql_provider.get_sql('get_cargo_info.sql', {'name': cargo_name})
            cursor.execute(sql_code)
            return cursor.fetchone()
        else:
            raise ValueError("ERROR. CURSOR NOT CREATED!")