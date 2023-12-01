#! /bin/python3

from flask import Flask, render_template, session
from os import urandom

from views.client_views import deliveries_app
from views.auth_views import auth_app
from views.profile_views import profile_app

app = Flask(__name__, static_folder='static', template_folder='templates')

app.register_blueprint(deliveries_app, url_prefix='/delivery')
app.register_blueprint(auth_app, url_prefix='/auth')
app.register_blueprint(profile_app, url_prefix='/profile')


@app.route('/')
def default_handler():
    logged = False
    staff = False
    if ('user_id' in session):
        logged = True
        if ('user_group' in session):
            staff = True
    return render_template('index.html', return_page_url=None, logged=logged, staff=staff)


if (__name__ == '__main__'):
    app.secret_key = urandom(32)
    app.run(host = '127.0.0.1', port = 5000, debug=True)