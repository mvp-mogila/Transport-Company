#! /bin/python3

from flask import Flask, render_template

from settings import secret_key

from views.client_views import deliveries_app
from views.auth_views import auth_app
# from views.profile_views import profile_app

app = Flask(__name__, static_folder='static', template_folder='templates')

app.register_blueprint(deliveries_app, url_prefix='/delivery')
app.register_blueprint(auth_app, url_prefix='/auth')


@app.route('/')
def default_handler():
    return render_template('index.html', return_page_url=None)


if (__name__ == '__main__'):
    app.secret_key = secret_key
    app.run(host = '127.0.0.1', port = 5000, debug=True)