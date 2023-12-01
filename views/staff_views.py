from flask import Blueprint, request, render_template, session

# from wrappers.access_control import group_required

staff_app = Blueprint('staff_app', template_folder='templates')


#@group_required
@staff_app.route('/info', methods=['GET'])
def default_info_hadler():
    return render_template('info.html', staff=True)


# @group_required
@staff_app.route('/info/clients', methods=['GET'])
def client_info_handler():
    return render_template('client-info.html', staff=True, return_page_url='/staff/info')


# @group_required
@staff_app.route('/info/staff', methods=['GET'])
def staff_info_handler():
    return render_template('staff-info.html', staff=True, return_page_url='/staff/info')


# @group_required
@staff_app.route('/info/clients', methods=['GET'])
def transport_info_handler():
    return render_template('transport-info.html', staff=True, return_page_url='/staff/info')


# @group_required
@staff_app.route('/info/clients', methods=['GET', 'POST'])
def delivery_info_handler():
    return render_template('delivery-info.html', staff=True, return_page_url='/staff/info')