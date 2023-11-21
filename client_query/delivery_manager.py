from database.connection import DBContextManager
from database.sql_provider import SQLProvider
from settings import db_config

sql_provider = SQLProvider('sql')
database = DBContextManager(db_config)

def all_user_deliveries(user_id):
    with database as cursor:
        if cursor:
            params = {'user_id': user_id}
            sql_code = sql_provider.get_sql('get_all_user_deliveries.sql', params)
            cursor.execute(sql_code)
            result = cursor.fetchall()
            return result
        else:
            raise ValueError("ERROR. CURSOR NOT CREATED!")

# def user_deliveries_by_date():


# def user_deliveries_by_status():


# def user_deliveries_by_weight():