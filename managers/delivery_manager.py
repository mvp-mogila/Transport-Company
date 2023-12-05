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


def get_delivery_info(delivery_id, user_id = None):
    with database as cursor:
        if cursor:
            if (user_id):
                params = {'id': delivery_id, 'client_id': user_id}
                if (delivery_id < 0):
                    return None, 400
                else:
                    sql_code = sql_provider.get_sql('get_client_delivery.sql', params)
            else:
                params = {'id': delivery_id}
                sql_code = sql_provider.get_sql('get_delivery.sql', params)
                
            cursor.execute(sql_code)
            result = cursor.fetchone()

            if (result is None):
                response_status = 404
            else:
                response_status = 200
        else:
            raise ValueError("ERROR. CURSOR NOT CREATED!")

    return result, response_status


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


def process_delivery(params):
     with database as cursor:
        if cursor:
            response_status = 200
            if (params.get('status') == 'Отменить'):
                sql_code = sql_provider.get_sql('cancel_delivery.sql', params)
            elif (params.get('manager') and params.get('driver') and params.get('transport') and params.get('status')):
                sql_code = sql_provider.get_sql('update_delivery.sql', params)
            else:
                response_status = 204
                return response_status
            rows_count = cursor.execute(sql_code)
                
            if (not rows_count):
                response_status = 500
            return response_status
        else:
            raise ValueError("ERROR. CURSOR NOT CREATED!")