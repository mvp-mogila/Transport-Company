#! /bin/python3

from flask import Flask, render_template


app = Flask(__name__, static_folder='static', template_folder='templates')


@app.route('/')
def default_handler():
    return render_template('index.html', return_page_url=None)


if (__name__ == '__main__'):
    app.run(host = '127.0.0.1', port = 5000, debug=True)