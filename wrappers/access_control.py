from flask import render_template, request, session, redirect, url_for
from functools import wraps
import json

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if ('user_id' in session):
            return func(*args, **kwargs)
        else:
            print(1234)
            return redirect(url_for('auth_app.login_handler'))
    return wrapper


# def group_required(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         if ('user_login' in session):
#             if ('user_group' in session):
#                 user_group = session.get('user_group')
#                 user_request = request.url.split('/')
#                 url = user_request[3]
#                 with open('access/access_config.json', 'r') as config:
#                     config_list = json.load(config)
#                     if user_group in config_list:
#                         if url in config_list[user_group]:
#                             return func(*args, **kwargs)
#                         else:
#                             return redirect('/', 403)
#             else:
#                 return redirect('/', 403)
#         else:
#             return redirect('/auth/login', 401)
#     return wrapper
