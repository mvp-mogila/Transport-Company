from datetime import date
import re

from database.connection import DBContextManager
from database.sql_provider import SQLProvider
from settings import db_config


sql_provider = SQLProvider('sql')
database = DBContextManager(db_config)


def get_user_deliveries(user_id, params):
    with database as cursor:
        if cursor:
            response_status = 200

            date_pattern = re.compile("^[0-9][1-9]\-[0-9][1-9]\-[1-2][0-9][0-9][0-9]")

            if (not params.get('send_date')):
                params['send_date'] = '01-01-1970'
            elif (not date_pattern.match(params.get('send_date'))):
                response_status = 400
            
            if (not params.get('delivery_date')):
                today = date.today()
                params['delivery_date'] = f'{today.day}-{today.month}-{today.year}'
            elif (not date_pattern.match(params.get('delivery_date'))):
                response_status = 400

            if (not params.get('weight_lower')):
                params['weight_lower'] = 0
            else:
                try:
                    int_weight = int(params.get('weight_lower'))
                    if (int_weight < 0):
                        response_status = 400
                except ValueError:
                    response_status = 400

            if (not params.get('weight_upper')):
                params['weight_upper'] = 1000000
            else:
                try:
                    int_weight = int(params.get('weight_upper'))
                    if (int_weight < 0):
                        response_status = 400
                except ValueError:
                    response_status = 400

            if (response_status != 400):
                params['user_id'] = user_id
                if (params.get('status')):
                    if (params.get('status') not in [ "Завершен", "В работе", "Отменен" ]):
                        response_status = 400
                    else:
                        sql_code = sql_provider.get_sql('get_user_deliveries_with_status.sql', params)
                else:
                    sql_code = sql_provider.get_sql('get_user_deliveries.sql', params)

                cursor.execute(sql_code)
                result = cursor.fetchall()

                if (result is None):
                    response_status = 404
            else:
                result = None
            return result, response_status
        else:
            raise ValueError("ERROR. CURSOR NOT CREATED!")


def get_delivery_info(delivery_id, user_id):
    with database as cursor:
        if cursor:
            params = {'id': delivery_id, 'user_id': user_id}
            response_status = 200
            result = {}
            
            if (delivery_id < 0):
                response_status = 400
                result = None
            else:
                sql_code = sql_provider.get_sql('get_delivery_information.sql', params)
                cursor.execute(sql_code)
                result = cursor.fetchall()

                if (result is None):
                    response_status = 404
        else:
            raise ValueError("ERROR. CURSOR NOT CREATED!")

    return result, response_status



# def create_new_delivery():
#     return None
