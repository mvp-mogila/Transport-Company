def create_rows(dict:dict, param:str):
    result = []
    for row in dict:
        result.append(row[param])
    return result