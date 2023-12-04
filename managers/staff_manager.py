from settings import database, sql_provider


def staff_info(user_id):
    with database as cursor:
        if (cursor):
            params = {'user_id': user_id}
            sql_code = sql_provider.get_sql('get_full_staff_info.sql', params)
            cursor.execute(sql_code)
            return cursor.fetchone()
        else:
            raise ValueError('ERROR. CURSOR NOT CREATED!')
        
    
def parse_group(group):
    if (group == 'Администратор'):
        return {'admin': 1, 'manager': 0, 'driver': 0}
    if (group == 'Экспедитор'):
        return {'admin': 0, 'manager': 1, 'driver': 0}
    if (group == 'Водитель'):
        return {'admin': 0, 'manager': 0, 'driver': 1}
    

def all_staff_info():
    with database as cursor:
        if (cursor):
            sql_code = sql_provider.get_sql('get_all_staffs_info.sql', dict())
            cursor.execute(sql_code)
            return cursor.fetchall()
        else:
            raise ValueError('ERROR. CURSOR NOT CREATED!')