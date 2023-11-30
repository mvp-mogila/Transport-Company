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
            session['user_id'] = user_info['id']
            if (user_info['staff_status']):
                session['user_group'] = user_info['staff_group']

            print(user_info)
            session.modified = True
            return redirect(url_for('default_handler'), 302)
        else:
            not_found = True
    return render_template('login.html', user_not_found = not_found, return_page_url = '/')


@auth_app.route('/sign-up', methods = ['GET', 'POST'])
def signup_handler():
    user_not_created = False
    if request.method == 'POST':
        login = request.form.get('login')
        user_id = user.check_user(login)

        if (not user_id):

            password = request.form.get('pass')
            name = request.form.get('name')
            surname = request.form.get('surname')
            fatherhood = request.form.get('fatherhood')
            phone_number = request.form.get('phone_number')
            address = request.form.get('address')

            user_info = { 'username': login,
                          'pass': password,
                          'name': name,
                          'surname': surname,
                          'fatherhood': fatherhood,
                          'telephone_number': phone_number,
                          'address': address }

            user.create_new_client(user_info)
            return redirect(url_for('default_handler'), 302)
        else:
            user_not_created = True
        
        
    return render_template('signup.html', user_not_created = user_not_created, return_page_url = '/')