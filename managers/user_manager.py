from flask import session

from settings import database, sql_provider


def validate_user(login, password):
    with database as cursor:
        if (login and password):
            params = {"login": login, "password": password}
            sql_code = sql_provider.get_sql('get_user_by_pass.sql', params)
            cursor.execute(sql_code)
            user_info = cursor.fetchone()
        else:
            raise ValueError("ERROR. CURSOR NOT CREATED!")
    return user_info
