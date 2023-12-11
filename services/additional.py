def create_rows(dict: dict, name: str, value:str):
    result = []
    for row in dict:
        result.append({"name": row[name], "value": row[value]})
    return result