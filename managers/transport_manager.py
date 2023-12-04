from settings import database, sql_provider


def all_transports_info():
    with database as cursor:
        if (cursor):
            sql_code = sql_provider.get_sql('get_all_transports_info.sql', dict())
            cursor.execute(sql_code)
            return cursor.fetchall()
        else:
            raise ValueError('ERROR. CURSOR NOT CREATED!')