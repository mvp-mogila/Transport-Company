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