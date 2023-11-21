#! /bin/python3

from flask import Flask, render_template

from client_query.client_deliveries import deliveries_app

app = Flask(__name__, static_folder='static', template_folder='templates')
app.register_blueprint(deliveries_app, url_prefix='/delivery')

@app.route('/')
def default_handler():
    return render_template('index.html', return_page_url=None)


if (__name__ == '__main__'):
    app.run(host = '127.0.0.1', port = 5000, debug=True)