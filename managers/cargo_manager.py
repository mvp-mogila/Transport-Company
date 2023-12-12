from http.client import FOUND, NOT_FOUND
from settings import database, sql_provider, cache


def get_cargo_info(cargo_id):
    with database as cursor:
        if (cursor):
            params = {'cargo_id': cargo_id}
            sql_code = sql_provider.get_sql('get_full_cargo_info.sql', params)
            cursor.execute(sql_code)
            result = cursor.fetchone()
            if (not result):
                return None, NOT_FOUND
            else:
                return result, FOUND
        else:
            raise ValueError('ERROR. CURSOR NOT CREATED!')
        

def get_all_cargos():
    cargo_list = cache.get_value('cargo_list')
    if (cargo_list):
        print(cargo_list)
        return cargo_list
    else:
        with database as cursor:
            if (cursor):
                sql_code = sql_provider.get_sql('get_all_cargo_info.sql', dict())
                cursor.execute(sql_code)
                result = cursor.fetchall()
                print(result)
                return result
            else:
                raise ValueError('ERROR. CURSOR NOT CREATED!')