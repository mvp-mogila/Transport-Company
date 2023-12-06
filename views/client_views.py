from http.client import BAD_REQUEST, NOT_FOUND
from flask import Blueprint, request, render_template, session
from werkzeug.exceptions import BadRequest, NotFound

from services.access_control import login_required
import managers.delivery_manager as delivery
import managers.user_manager as user


deliveries_app = Blueprint('deliveries_app', __name__, template_folder="templates")


@deliveries_app.route('/', methods=["GET"])
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
                       {'name': "Статус", 'params': ["Завершен", "В работе", "Отменен"], 'arg': 'status', 'type': None} ]

    return render_template('deliveries.html', all=True, user_deliveries=deliveries, form_method=form_method,
             options=search_options, button_title=button_title, staff=False, logged=True, return_url='/'), response_code


@login_required
@deliveries_app.route('/<int:delivery_id>')
def delivery_handler(delivery_id):
    user_id = session.get('user_id')
    params = {'user_id': user_id, 'delivery_id': delivery_id}
    print(params)
    delivery_details, response_code = delivery.get_user_delivery(params)

    if (response_code == NOT_FOUND):
        raise NotFound

    return render_template('delivery-details.html', delivery=delivery_details, return_url='/delivery/'), response_code
