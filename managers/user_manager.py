from settings import database, sql_provider


def validate_user(login, password):
    with database as cursor:
        if (cursor):
            params = {'username': login, 'pass': password}
            sql_code = sql_provider.get_sql('get_user_by_pass.sql', params)
            cursor.execute(sql_code)
            user_info = cursor.fetchone()
            if (user_info['staff_status']):
                sql_code = sql_provider.get_sql('get_staff_by_user_id.sql', {'user_id': user_info['id']})
                cursor.execute(sql_code)
                staff_group = cursor.fetchone()
                user_info['staff_group'] = staff_group['position']
        else:
            raise ValueError("ERROR. CURSOR NOT CREATED!")
    return user_info


def check_user(login):
    with database as cursor:
        if (cursor):
            params = {'username': login}
            sql_code = sql_provider.get_sql('get_user_by_login.sql', params)
            cursor.execute(sql_code)
            user_id = cursor.fetchone()
        else:
            raise ValueError("ERROR. CURSOR NOT CREATED!")
    return user_id


def create_new_client(params):
    with database as cursor:
        if (cursor):
            sql_code = sql_provider.get_sql('create_user.sql', params)
            rows_count = cursor.execute(sql_code)
            if (rows_count != 1):
                raise ValueError("ERROR. INSERTION CANCELLED!")
            sql_code = sql_provider.get_sql('get_user_by_login.sql', params)
            rows_count = cursor.execute(sql_code)
            if (rows_count != 1):
                raise ValueError("ERROR. INSERTION CANCELLED!")
            user_id = cursor.fetchone()
            params['user_id'] = user_id['id']
            sql_code = sql_provider.get_sql('create_client.sql', params)
            rows_count = cursor.execute(sql_code)
            if (rows_count != 1):
                raise ValueError("ERROR. INSERTION CANCELLED!")
        else:
            raise ValueError("ERROR. CURSOR NOT CREATED!")
        

def user_info(user_id):
    with database as cursor:
        if (cursor):
            params = {'id': user_id}
            sql_code = sql_provider.get_sql('get_full_user_info.sql', params)
            cursor.execute(sql_code)
            return cursor.fetchone()
        else:
            raise ValueError("ERROR. CURSOR NOT CREATED!")
