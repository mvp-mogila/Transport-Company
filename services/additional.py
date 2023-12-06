def create_rows(dict: dict, param: str):
    result = []
    for row in dict:
        result.append(row[param])
    return result


def convert_date(date: str):
    return 'STR_TO_DATE(' + date + ', "%Y-%m-%d")'