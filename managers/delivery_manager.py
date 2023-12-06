from http.client import BAD_REQUEST, NO_CONTENT, NOT_FOUND, OK
import re

from settings import database, sql_provider
from services.additional import convert_date

def get_user_deliveries(params):
    with database as cursor:
        if cursor:
            if (not params.get('weight_lower')):
                params['weight_lower'] = 0
            else:
                try:
                    int_weight = int(params.get('weight_lower'))
                    (int_weight >= 0)
                except ValueError or AssertionError:
                    return None, BAD_REQUEST

            if (not params.get('weight_upper')):
                params['weight_upper'] = 1000000
            else:
                try:
                    int_weight = int(params.get('weight_upper'))
                    (int_weight >= 0)
                except ValueError or AssertionError:
                    return None, BAD_REQUEST

            if (not params.get('status')):
                params['status'] = '%'
            elif (params.get('status') not in ["Завершен", "В работе", "Отменен"]):
                return None, BAD_REQUEST

            sql_code = sql_provider.get_sql('get_client_deliveries.sql', params)
            cursor.execute(sql_code)
            result = cursor.fetchall()
            if (not result):
                return None, NO_CONTENT
            return result, OK
        else:
            raise ValueError("ERROR. CURSOR NOT CREATED!")


def get_user_delivery(params):
    with database as cursor:
        if cursor:
            sql_code = sql_provider.get_sql('get_client_delivery.sql', params)
            print(sql_code)
            cursor.execute(sql_code)
            result = cursor.fetchone()
            print(12312312312)
            if (not result):
                return None, NOT_FOUND
            else:
                return result, OK
        else:
            raise ValueError("ERROR. CURSOR NOT CREATED!")


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

            if (params.get('send_date')):
                if (date_pattern.match(params.get('send_date'))):
                    params['send_date'] = convert_date(params.get('send_date'))
                else:
                    response_status = 400
            else:
                params['send_date'] = '%'
            
            if (params.get('delivery_date')):
                if (date_pattern.match(params.get('delivery_date'))):
                    params['delivery_date'] = convert_date(params.get('delivery_date'))
                else:
                    response_status = 400
            else:
                params['delivery_date'] = '%'

            if (params.get('status')):
                if (params.get('status') not in ["Завершен", "В работе", "Отменен"]):
                    response_status = 400
            else:
                params['status'] = '%'

            if (response_status != 400):
                sql_code = sql_provider.get_sql('get_all_deliveries_info.sql', params)
                cursor.execute(sql_code)
                result = cursor.fetchall()
                
                if (not result):
                    response_status = 404
                else:
                    return result, response_status
            else:
                return None, response_status
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