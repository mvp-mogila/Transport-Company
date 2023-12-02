from settings import database, sql_provider


def client_info(user_id):
    with database as cursor:
        if (cursor):
            params = {'user_id': user_id}
            sql_code = sql_provider.get_sql('get_full_client_info.sql', params)
            cursor.execute(sql_code)
            return cursor.fetchone()
        else:
            raise ValueError('ERROR. CURSOR NOT CREATED!')
        

def all_clients_info():
    with database as cursor:
        if (cursor):
            sql_code = sql_provider.get_sql('get_all_clients_info.sql', dict())
            cursor.execute(sql_code)
            return cursor.fetchall()
        else:
            raise ValueError('ERROR. CURSOR NOT CREATED!')