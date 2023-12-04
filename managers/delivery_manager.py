from queue import Empty
import re

from settings import database, sql_provider


def get_user_deliveries(user_id, params):
    with database as cursor:
        if cursor:
            response_status = 200

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
                    params['status'] = 'Завершен'

                sql_code = sql_provider.get_sql('get_client_deliveries.sql', params)
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


def count_deliveries(clients):
    with database as cursor:
        if (cursor):
            for client in clients:
                params = {'client_id': client['doc_num']}
                sql_code = sql_provider.get_sql('count_client_deliveries.sql',params)
                cursor.execute(sql_code)
                result = cursor.fetchone()
                client['deliveries_count'] = result['total_deliveries']
            return clients
        else:
            raise ValueError("ERROR. CURSOR NOT CREATED!")
        

def all_deliveries_info(params):
    with database as cursor:
        if cursor:
            response_status = 200

            date_pattern = re.compile("^((0[1-9])|([1-2][0-9])|(3[0-1]))\-((0[1-9])|(1[0-2]))\-(20[0-2][0-9])")

            if (params.get('send_date') and not date_pattern.match(params.get('send_date'))):
                response_status = 400
            
            if (params.get('delivery_date') and not date_pattern.match(params.get('delivery_date'))):
                response_status = 400

            if (response_status != 400):
                if (params.get('status')):
                    if (params.get('status') not in [ "Завершен", "В работе", "Отменен" ]):
                        response_status = 400
                else:
                    params['status'] = 'Завершен'

            if (response_status != 400):
                if (params.get('send_date') and params.get('delivery_date')):
                    sql_code = sql_provider.get_sql('get_all_deliveries_info_with_send_delivery_date.sql', params)
                elif (params.get('send_date') and not params.get('delivery_date')):
                    sql_code = sql_provider.get_sql('get_all_deliveries_info_with_send_date.sql', params)
                elif (not params.get('send_date') and params.get('delivery_date')):
                    sql_code = sql_provider.get_sql('get_all_deliveries_info_with_delivery_date.sql', params)
                else:
                    sql_code = sql_provider.get_sql('get_all_deliveries_info.sql', params)

                cursor.execute(sql_code)
                result = cursor.fetchall()
                
                if (not result):
                    response_status = 404
            else:
                result = None
            return result, response_status
        else:
            raise ValueError("ERROR. CURSOR NOT CREATED!")
