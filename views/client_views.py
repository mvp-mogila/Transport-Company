from http.client import BAD_REQUEST, CONFLICT, CREATED, NOT_FOUND
from flask import Blueprint, request, render_template, session, redirect, url_for
from werkzeug.exceptions import BadRequest, NotFound, Conflict

from services.access_control import login_required
import managers.delivery_manager as delivery
from views.item_views import items_app

client_app = Blueprint('client_app', __name__, template_folder="templates")
client_app.register_blueprint(items_app, url_prefix='/items')

@client_app.route('/', methods=["GET"])
@login_required
def deliveries_handler():
    delivery_id = request.args.get('delivery_id')
    weight_lower = request.args.get('weight_lower')
    weight_upper = request.args.get('weight_upper')
    status = request.args.get('status')

    user_id = session.get('user_id')

    deliveries, response_code = delivery.get_user_deliveries( { 'user_id': user_id,
                                        'delivery_id': delivery_id, 'status': status,
                                        'weight_lower': weight_lower, 'weight_upper': weight_upper})

    if (response_code == BAD_REQUEST):
        raise BadRequest

    form_method = "GET"
    button_title = "Поиск"
    search_options = [ {'name': "Номер заказа", 'params': None, 'arg': 'delivery_id', 'type': 'number'},
                       {'name': "Вес (от)", 'params': None, 'arg': 'weight_lower', 'type': 'number'},
                       {'name': "Вес (до)", 'params': None, 'arg': 'weight_upper', 'type': 'number'},
                       {'name': "Статус", 'params': [{"name": "Завершен", "value": "Завершен"},
                                    {"name": "В работе", "value": "В работе"}, {"name": "Отменен", "value": "Отменен"}],
                                    'arg': 'status', 'type': None} ]

    return render_template('deliveries.html', all=True, user_deliveries=deliveries, form_method=form_method,
             options=search_options, button_title=button_title, staff=False, logged=True, return_url='/'), response_code


@client_app.route('/<int:delivery_id>')
@login_required
def delivery_handler(delivery_id):
    user_id = session.get('user_id')
    params = {'user_id': user_id, 'delivery_id': delivery_id}
    print(params)
    delivery_details, response_code = delivery.get_user_delivery(params)

    if (response_code == NOT_FOUND):
        raise NotFound

    return render_template('delivery-details.html', delivery=delivery_details, return_url='/delivery/'), response_code


@client_app.route('new', methods=['GET', 'POST'])
@login_required
def new_delivery_handler():



    if (request.method == 'POST'):

        if (not session.get('items')):
            return redirect(url_for('client_app.items_app.default_order_handler'))

        user_id = session.get('user_id')
        send_date = request.form.get('send_date')
        delivery_date = request.form.get('delivery_date')
        send_address = request.form.get('send_address')
        delivery_address = request.form.get('delivery_address')

        params = {'user_id': user_id, 'send_date': send_date, 'delivery_date': delivery_date,
                  'send_address': send_address, 'delivery_address': delivery_address}

        
        # delivery_id, response_code = delivery.create_delivery(params)
        
        # if (response_code ==  BAD_REQUEST):
        #     raise BadRequest
        # elif (response_code == CREATED):
            
        #     session['delivery_id'] = delivery_id
        #     session['items'] = {}
        #     session.modified = True
            

    return render_template('new-delivery.html', logged=True, return_url='/')


