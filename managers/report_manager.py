from http.client import BAD_REQUEST, CONFLICT, CREATED, NO_CONTENT, NOT_FOUND, OK, NOT_FOUND, UNPROCESSABLE_ENTITY
import re

from settings import database, sql_provider


def validate_report_params(params, set_default = 0):
    if (not params.get('cargo_name')):
        if (set_default):
            params['cargo_name'] = '%'
        else:
            return None, UNPROCESSABLE_ENTITY
    elif (params.get('cargo_name') not in ["Малая коробка", "Средняя коробка", "Большая коробка", "Крупный груз", "Насыпной груз"]):
        return None, BAD_REQUEST

    date_pattern = re.compile("^(20[0-2][0-9])\-((0[1-9])|(1[0-2]))")

    if (not params.get('date')):
        if (set_default):
            params['year'] = '%'
            params['month'] = '%'
        else:
            return None, UNPROCESSABLE_ENTITY
    elif (params.get('date') and not date_pattern.match(params.get('date'))):
        return None, BAD_REQUEST
    else:
        date = params.get('date').split('-')
        params['year'] = date[0]
        params['month'] = date[1]

    return params, OK


def report_info(params):
    with database as cursor:
        if cursor:
            params, response_code = validate_report_params(params, set_default=1)

            if (response_code == BAD_REQUEST):
                return None, BAD_REQUEST
            
            sql_code = sql_provider.get_sql('get_report.sql', params)
            cursor.execute(sql_code)
            result = cursor.fetchall()

            if (not result):
                return None, NOT_FOUND
            else:
                return result, OK
        else:
            raise ValueError("ERROR. CURSOR NOT CREATED!")
        

def create_report(params):
    with database as cursor:
        if cursor:
            params, response_code = validate_report_params(params)

            if (response_code == BAD_REQUEST):
                return BAD_REQUEST
            elif (response_code == UNPROCESSABLE_ENTITY):
                return UNPROCESSABLE_ENTITY
            
            sql_code = sql_provider.get_sql('get_report.sql', params)
            if (cursor.execute(sql_code)):
                return CONFLICT

            sql_code = sql_provider.get_sql('check_cargo_sales.sql', params)
            if (not cursor.execute(sql_code)):
                return NO_CONTENT
            sql_code = cursor.callproc('create_report', [params['cargo_name'], params['year'], params['month']])
            return CREATED
        else:
            raise ValueError("ERROR. CURSOR NOT CREATED!")