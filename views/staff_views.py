from flask import Blueprint, request, render_template, session

# from wrappers.access_control import group_required
import managers.staff_manager as staff
import managers.client_manager as client
import managers.transport_manager as transport
import managers.delivery_manager as delivery

staff_app = Blueprint('staff_app', __name__, template_folder='templates')


#@group_required
@staff_app.route('/info', methods=['GET'])
def default_info_handler():
    user_group = session.get('user_group')
    group = staff.parse_group(user_group)
    return render_template('info.html', group=group, staff=True, return_page_url='/', logged=True), 200


# @group_required
@staff_app.route('/info/clients', methods=['GET'])
def client_info_handler():
    user_group = session.get('user_group')
    group = staff.parse_group(user_group)
    clients = client.all_clients_info()
    response_code = 200
    if (clients):
        clients = delivery.count_deliveries(clients)
    else:
        response_code = 404
    return render_template('info.html', group=group, staff=True, clients=clients,
                           return_page_url='/staff/info', logged=True), response_code


# @group_required
@staff_app.route('/info/staff', methods=['GET'])
def staff_info_handler():
    user_group = session.get('user_group')
    group = staff.parse_group(user_group)
    staffs = staff.all_staff_info()
    response_code = 200
    if (not staffs):
        response_code = 404
    return render_template('info.html', group=group, staff=True, staffs=staffs,
                           return_page_url='/staff/info', logged=True), response_code


# @group_required
@staff_app.route('/info/transport', methods=['GET'])
def transport_info_handler():
    user_group = session.get('user_group')
    group = staff.parse_group(user_group)
    transports = transport.all_transport_info()
    response_code = 200
    if (not transports):
        response_code = 404
    return render_template('info.html', group=group, staff=True, transports=transports,
                           return_page_url='/staff/info', logged=True), response_code


# @group_required
@staff_app.route('/info/deliveries', methods=['GET', 'POST'])
def delivery_info_handler():
    user_group = session.get('user_group')
    group = staff.parse_group(user_group)
    return render_template('info.html', group=group, staff=True, delivery_info=True,
                           return_page_url='/staff/info')