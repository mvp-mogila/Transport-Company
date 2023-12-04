from http.client import NOT_FOUND
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
    return render_template('info.html', group=group, staff_status=True, return_page_url='/', logged=True), 200


# @group_required
@staff_app.route('/info/clients', methods=['GET'])
def client_info_handler():
    user_group = session.get('user_group')
    group = staff.parse_group(user_group)
    clients = client.all_clients_info()
    response_code = 200
    not_found = False
    if (clients):
        clients = delivery.count_deliveries(clients)
    else:
        response_code = 404
        not_found = True
    return render_template('info.html', group=group, staff_status=True, clients=clients,
                           return_page_url='/', logged=True, not_found=not_found), response_code


# @group_required
@staff_app.route('/info/staff', methods=['GET'])
def staff_info_handler():
    user_group = session.get('user_group')
    group = staff.parse_group(user_group)
    staffs = staff.all_staffs_info()
    response_code = 200
    not_found = False
    if (not staffs):
        response_code = 404
        not_found = True
    return render_template('info.html', group=group, staff_status=True, staffs=staffs,
                           return_page_url='/', logged=True, not_found=not_found), response_code


# @group_required
@staff_app.route('/info/transport', methods=['GET'])
def transport_info_handler():
    user_group = session.get('user_group')
    group = staff.parse_group(user_group)
    transports = transport.all_transports_info()
    response_code = 200
    not_found = False
    if (not transports):
        response_code = 404
        not_found = True
    print(transports)
    return render_template('info.html', group=group, staff_status=True, transports=transports,
                           return_page_url='/', logged=True, not_found=not_found), response_code


# @group_required
@staff_app.route('/info/deliveries', methods=['GET'])
def delivery_info_handler():
    user_group = session.get('user_group')
    group = staff.parse_group(user_group)

    send_date = request.args.get('send_date')
    deliv_date = request.args.get('delivery_date')
    status = request.args.get('status')

    deliveries, response_code = delivery.all_deliveries_info({'send_date': send_date, 
                                                                'delivery_date': deliv_date,
                                                                'status': status})
    not_found = False
    print(response_code)
    if (response_code == 400):
        return "<center><h1>Некорректный запрос</h1></center>", response_code
    elif (response_code == 404):
        not_found = True

    search_options = [{'name': "Дата отправки dd-mm-yyy", 'params': None, 'arg': 'send_date'},
                      {'name': "Дата доставки dd-mm-yyy", 'params': None, 'arg': 'delivery_date'},
                      {'name': "Статус", 'params': ["Завершен", "В работе", "Отменен"], 'arg': 'status'}]
    
    return render_template('info.html', group=group, staff_status=True, deliveries=deliveries,
                           return_page_url='/', logged=True, search_options=search_options, not_found=not_found), response_code