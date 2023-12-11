#! /bin/python3

from http.client import BAD_REQUEST, NOT_FOUND, FORBIDDEN
from flask import Flask, render_template, session
from werkzeug.exceptions import BadRequest, NotFound, Forbidden
from os import urandom

from views.client_views import client_app
from views.auth_views import auth_app
from views.profile_views import profile_app
from views.staff_views import staff_app

app = Flask(__name__, static_folder='static', template_folder='templates')

app.register_blueprint(client_app, url_prefix='/delivery')
app.register_blueprint(auth_app, url_prefix='/auth')
app.register_blueprint(profile_app, url_prefix='/profile')
app.register_blueprint(staff_app, url_prefix='/staff')


@app.errorhandler(BadRequest)
def handle_bad_request(e):
    title = f'{e.code} Некорректный запрос'
    return render_template('error.html', title=title), BAD_REQUEST


@app.errorhandler(NotFound)
def handle_bad_request(e):
    title = f'{e.code} Не найдено'
    return render_template('error.html', title=title), NOT_FOUND


@app.errorhandler(Forbidden)
def handle_forbidden(e):
    title = f'{e.code} Доступ запрещен'
    return render_template('error.html', title=title), FORBIDDEN


@app.route('/')
def default_handler():
    logged = False
    staff = False
    if ('user_id' in session):
        logged = True
        if ('user_group' in session):
            staff = True
    return render_template('index.html', logged=logged, staff_status=staff)


if (__name__ == '__main__'):
    app.secret_key = urandom(32)
    app.run(host = '127.0.0.1', port = 5000, debug=True)