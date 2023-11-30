from flask import Blueprint, redirect, request, render_template, session, url_for

from managers import user_manager as user

auth_app = Blueprint('auth_app', __name__, template_folder="templates")

@auth_app.route('/login', methods = ['GET'])
def login_handler():
    not_found = False
    login = request.args.get('login')
    password = request.args.get('pass')
    if (login and password):
        user_info = user.validate_user(login, password)
        if (user_info):
            session["user_id"] = user_info['id']
            session.modified = True
            return redirect(url_for('default_handler'), 302)
        else:
            not_found = True
    return render_template('login.html', user_not_found = not_found, return_page_url = '/')