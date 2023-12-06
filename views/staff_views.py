from http.client import NOT_FOUND, BAD_REQUEST
from werkzeug.exceptions import NotFound, BadRequest
from flask import Blueprint, request, render_template, session

from services.additional import create_rows
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
    return render_template('info.html', group=group, staff_status=True, return_url='/', logged=True)


# @group_required
@staff_app.route('/info/clients', methods=['GET'])
def client_info_handler():
    user_group = session.get('user_group')
    group = staff.parse_group(user_group)
    clients = client.all_clients_info()
    if (clients):
        clients = delivery.count_deliveries(clients)
    else:
        raise NotFound
    return render_template('info.html', group=group, staff_status=True, clients=clients, logged=True, return_url='/')


# @group_required
@staff_app.route('/info/staff', methods=['GET'])
def staff_info_handler():
    user_group = session.get('user_group')
    group = staff.parse_group(user_group)
    staffs = staff.all_staffs_info()
    if (not staffs):
        raise NotFound
    return render_template('info.html', group=group, staff_status=True, staffs=staffs, return_url='/', logged=True)


# @group_required
@staff_app.route('/info/transport', methods=['GET'])
def transport_info_handler():
    user_group = session.get('user_group')
    group = staff.parse_group(user_group)
    transports = transport.all_transports_info()
    if (not transports):
        raise NotFound
    return render_template('info.html', group=group, staff_status=True, transports=transports, return_url='/', logged=True)


# @group_required
@staff_app.route('/info/deliveries', methods=['GET'])
def delivery_info_handler():
    user_group = session.get('user_group')
    group = staff.parse_group(user_group)

    delivery_id = request.args.get('delivery_id')
    send_date = request.args.get('send_date')
    deliv_date = request.args.get('delivery_date')
    status = request.args.get('status')

    deliveries, response_code = delivery.all_deliveries_info({'delivery_id': delivery_id,
                    'send_date': send_date, 'delivery_date': deliv_date, 'status': status})
    
    if (response_code == BAD_REQUEST):
        raise BadRequest

    form_method = "GET"
    button_title = "Поиск"
    search_options = [ {'name': "Номер доставки", 'params': None, 'arg': 'delivery_id', 'type': 'number'},
                {'name': "Дата отправки", 'params': None, 'arg': 'send_date', 'type': 'date'},
                {'name': "Дата доставки", 'params': None, 'arg': 'delivery_date', 'type': 'date'},
                {'name': "Статус", 'params': ["Завершен", "В работе", "Отменен"], 'arg': 'status', 'type': None} ]
    
    return render_template('info.html', group=group, staff_status=True, deliveries=deliveries,form_method=form_method,
                           options=search_options, button_title=button_title, logged=True, return_url='/')


# @group_required
@staff_app.route('/delivery/process/<int:delivery_id>', methods=['GET', 'POST'])
def delivery_process_handler(delivery_id):
    user_group = session.get('user_group')
    group = staff.parse_group(user_group)

    managers_list = staff.get_managers()
    drivers_list = staff.get_drivers()
    transports_list = transport.get_ready_trasnport()

    managers = create_rows(managers_list, 'id')
    drivers = create_rows(drivers_list, 'id')
    transports = create_rows(transports_list, 'id')
    

    delivery_info, response_code = delivery.get_delivery_info(delivery_id)

    not_found = False
    if (response_code == 400):
        return "<center><h1>Некорректный запрос</h1></center>", response_code
    elif (response_code == 404):
        not_found = True

    options = [ {'name': "Экспедитор", 'params': managers, 'arg': 'manager'},
                {'name': "Водитель", 'params': drivers, 'arg': 'driver'},
                {'name': "Автомобиль", 'params': transports, 'arg': 'transport'},
                {'name': "Статус", 'params': ['Взять в работу', 'Отменить', 'Завершить'], 'arg': 'status'} ]

    not_set = False
    if (request.method == 'POST'):
        manager_id = request.form.get('manager')
        driver_id = request.form.get('driver')
        transport_id = request.form.get('transport')
        status = request.form.get('status')

        params = {'id': delivery_id, 'manager': manager_id, 'driver': driver_id, 'transport': transport_id, 'status':status}

        response_code = delivery.process_delivery(params)

        if (response_code == 204):
            not_set = True

    return render_template('delivery-process.html', group=group, staff_status=True, delivery=delivery_info,
                            return_page_url='/staff/info', logged=True, options=options, not_found=not_found, not_set=not_set), response_code
