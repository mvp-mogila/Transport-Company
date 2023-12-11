from http.client import BAD_REQUEST, NO_CONTENT, NOT_FOUND, OK
import re
from xmlrpc.client import SERVER_ERROR

from settings import database, sql_provider

def get_user_deliveries(params):
    with database as cursor:
        if cursor:
            if (not params.get('delivery_id')):
                params['delivery_id'] = '%'
            else:
                try:
                    int(params.get('delivery_id'))
                except ValueError:
                    return None, BAD_REQUEST
                

            if (not params.get('weight_lower')):
                params['weight_lower'] = 0
            else:
                try:
                    int(params.get('weight_lower'))
                except ValueError:
                    return None, BAD_REQUEST

            if (not params.get('weight_upper')):
                params['weight_upper'] = 1000000
            else:
                try:
                    int(params.get('weight_upper'))
                except ValueError:
                    return None, BAD_REQUEST

            if (not params.get('status')):
                params['status'] = '%'
            elif (params.get('status') not in ["Завершен", "В работе", "Отменен"]):
                return None, BAD_REQUEST

            sql_code = sql_provider.get_sql('get_client_deliveries.sql', params)
            cursor.execute(sql_code)
            result = cursor.fetchall()
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
            if (not result):
                return None, NOT_FOUND
            else:
                return result, OK
        else:
            raise ValueError("ERROR. CURSOR NOT CREATED!")


def count_deliveries(clients):
    with database as cursor:
        if cursor:
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
            if (not params.get('delivery_id')):
                params['delivery_id'] = '%'
            else:
                try:
                    int(params.get('delivery_id'))
                except ValueError:
                    return None, BAD_REQUEST

            if (params['delivery_id'] != '%'):
                sql_code = sql_provider.get_sql('get_all_delivery_info.sql', params)
                cursor.execute(sql_code)
                result = cursor.fetchall()

                if (not result):
                    return None, NOT_FOUND
                else:
                    return result, OK

            date_pattern = re.compile("^(20[0-2][0-9])\-((0[1-9])|(1[0-2]))\-((0[1-9])|([1-2][0-9])|(3[0-1]))")

            if (params.get('send_date') and not date_pattern.match(params.get('send_date'))):
                return None, BAD_REQUEST
                
            if (params.get('delivery_date') and not date_pattern.match(params.get('delivery_date'))):
                return None, BAD_REQUEST

            if (not params.get('status')):
                params['status'] = '%'
            elif (params.get('status') not in ["Завершен", "В работе", "Отменен"]):
                return None, BAD_REQUEST

            if (params.get('send_date') and params.get('delivery_date')):
                sql_code = sql_provider.get_sql('get_all_deliveries_info_with_send_delivery_dates.sql', params)
            elif (params.get('send_date') and not params.get('delivery_date')):
                sql_code = sql_provider.get_sql('get_all_deliveries_info_with_send_date.sql', params)
            elif (not params.get('send_date') and params.get('delivery_date')):
                sql_code = sql_provider.get_sql('get_all_deliveries_info_with_delivery_date.sql', params)
            else:
                sql_code = sql_provider.get_sql('get_all_deliveries_info.sql', params)

            cursor.execute(sql_code)
            result = cursor.fetchall()

            if (not result):
                return None, NOT_FOUND
            else:
                return result, OK
        else:
            raise ValueError("ERROR. CURSOR NOT CREATED!")


def process_delivery(params):
    with database as cursor:
        if cursor:
            if (params.get('status') not in ["Завершить", "Взять в работу", "Отменить"]):
                return BAD_REQUEST
            elif (params.get('status') == "Отменить"):
                sql_code = sql_provider.get_sql('cancel_delivery.sql', params)
            elif (params.get('status') == "Завершить"):
                sql_code = sql_provider.get_sql('finish_delivery.sql', params)
            elif (params.get('manager') and params.get('driver') and params.get('transport') and params.get('status')):
                sql_code = sql_provider.get_sql('update_delivery.sql', params)
            else:
                return NO_CONTENT

            if (not cursor.execute(sql_code)):
                return SERVER_ERROR
            else:
                return OK
        else:
            raise ValueError("ERROR. CURSOR NOT CREATED!")

