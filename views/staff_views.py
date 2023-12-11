from http.client import NO_CONTENT, NOT_FOUND, BAD_REQUEST, OK
from werkzeug.exceptions import NotFound, BadRequest
from flask import Blueprint, redirect, request, render_template, session, url_for

from services.additional import create_rows
from services.access_control import group_required
import managers.staff_manager as staff
import managers.client_manager as client
import managers.transport_manager as transport
import managers.delivery_manager as delivery
from views.report_views import report_app


staff_app = Blueprint('staff_app', __name__, template_folder='templates')
staff_app.register_blueprint(report_app, url_prefix="/report")


@staff_app.route('/info', methods=['GET'])
@group_required
def default_info_handler():
    user_group = session.get('user_group')
    group = staff.parse_group(user_group)
    return render_template('info.html', group=group, staff_status=True, return_url='/', logged=True)



@staff_app.route('/info/clients', methods=['GET'])
@group_required
def client_info_handler():
    user_group = session.get('user_group')
    group = staff.parse_group(user_group)
    clients = client.all_clients_info()
    if (clients):
        clients = delivery.count_deliveries(clients)
    else:
        raise NotFound
    return render_template('info.html', group=group, staff_status=True, clients=clients, logged=True, return_url='/')


@staff_app.route('/info/staff', methods=['GET'])
@group_required
def staff_info_handler():
    user_group = session.get('user_group')
    group = staff.parse_group(user_group)
    staffs = staff.all_staffs_info()
    if (not staffs):
        raise NotFound
    return render_template('info.html', group=group, staff_status=True, staffs=staffs, return_url='/', logged=True)


@staff_app.route('/info/transport', methods=['GET'])
@group_required
def transport_info_handler():
    user_group = session.get('user_group')
    group = staff.parse_group(user_group)
    transports = transport.all_transports_info()
    if (not transports):
        raise NotFound
    return render_template('info.html', group=group, staff_status=True, transports=transports, return_url='/', logged=True)


@staff_app.route('/info/deliveries', methods=['GET'])
@group_required
def delivery_info_handler():
    user_group = session.get('user_group')
    group = staff.parse_group(user_group)

    delivery_id = request.args.get('delivery_id')
    send_date = request.args.get('send_date')
    deliv_date = request.args.get('delivery_date')
    status = request.args.get('status')

    deliveries, response_code = delivery.all_deliveries_info({'delivery_id': delivery_id,
                    'send_date': send_date, 'delivery_date': deliv_date, 'status': status})
    
    deliveries_not_found = False
    if (response_code == BAD_REQUEST):
        raise BadRequest
    if (response_code == NOT_FOUND):
        deliveries_not_found = True

    form_method = "GET"
    button_title = "Поиск"
    search_options = [ {'name': "Номер доставки", 'params': None, 'arg': 'delivery_id', 'type': 'number'},
                {'name': "Дата отправки", 'params': None, 'arg': 'send_date', 'type': 'date'},
                {'name': "Дата доставки", 'params': None, 'arg': 'delivery_date', 'type': 'date'},
                {'name': "Статус", 'params': [{"name": "Завершен"}, {"name": "В работе"}, {"name": "Отменен"}], 'arg': 'status', 'type': None} ]
    
    return render_template('info.html', group=group, staff_status=True, deliveries=deliveries,form_method=form_method,
            deliveries_not_found=deliveries_not_found, options=search_options, button_title=button_title, logged=True, return_url='/')


@staff_app.route('/delivery/process/<int:delivery_id>', methods=['GET', 'POST'])
@group_required
def delivery_process_handler(delivery_id):
    user_group = session.get('user_group')
    group = staff.parse_group(user_group)

    managers_list = staff.get_managers()
    drivers_list = staff.get_drivers()
    transports_list = transport.get_ready_trasnport()

    managers = create_rows(managers_list, 'surname', 'id')
    drivers = create_rows(drivers_list, 'surname', 'id')
    transports = create_rows(transports_list, 'model', 'id')
    
    delivery_info, response_code = delivery.all_deliveries_info({'delivery_id': delivery_id})

    not_found = False
    if (response_code == BAD_REQUEST):
        raise BadRequest
    if (response_code == NOT_FOUND):
        raise NotFound

    form_method = "POST"
    button_title = "Подтвердить"
    options = [ {'name': "Экспедитор", 'params': managers, 'arg': 'manager', 'type': None},
                {'name': "Водитель", 'params': drivers, 'arg': 'driver', 'type': None},
                {'name': "Автомобиль", 'params': transports, 'arg': 'transport', 'type': None},
                {'name': "Статус", 'params': [
                    {"name": "Взять в работу", "value": "Взять в работу"},
                    {"name": "Отменить", "value": "Отменить"}, {"name": "Завершить", "value": "Завершить"}], 'arg': 'status', 'type': None}]

    not_set = False
    if (request.method == 'POST'):
        manager_id = request.form.get('manager')
        driver_id = request.form.get('driver')
        transport_id = request.form.get('transport')
        status = request.form.get('status')

        params = {'id': delivery_id, 'manager': manager_id, 'driver': driver_id, 'transport': transport_id, 'status': status}

        response_code = delivery.process_delivery(params)
        
        if (response_code == BAD_REQUEST):
            raise BadRequest
        elif (response_code == NO_CONTENT):
            not_set = True
        elif (response_code == OK):
            return redirect(url_for('staff_app.delivery_info_handler'))
        
    return render_template('delivery-process.html', group=group, staff_status=True, delivery=delivery_info[0],
                form_method=form_method, button_title=button_title, options=options, 
                return_url='/staff/info', logged=True, not_found=not_found, not_set=not_set)
