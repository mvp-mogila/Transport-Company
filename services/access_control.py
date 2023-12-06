from flask import session, redirect, url_for, request
from functools import wraps
import json
from werkzeug.exceptions import Forbidden


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if ('user_id' in session):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('auth_app.login_handler'))
    return wrapper


def group_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if ('user_id' in session):
            if ('user_group' in session):
                user_group = session.get('user_group')
                app = request.blueprint
                function = request.endpoint
                with open('services/access_config.json', 'r') as config_file:
                    config = json.load(config_file)
                    if (user_group in config and app in config[user_group]):
                        return func(*args, **kwargs)
                    elif (user_group in config and function in config[user_group]):
                        return func(*args, **kwargs)
                    else:
                        raise Forbidden
            else:
                raise Forbidden
        else:
            return redirect(url_for('auth_app.login_handler'))
    return wrapper