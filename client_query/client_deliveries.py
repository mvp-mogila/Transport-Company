from flask import Blueprint, request, render_template

import client_query.delivery_manager as query

deliveries_app = Blueprint('deliveries_app', __name__, template_folder = "templates")


@deliveries_app.route('/', methods=["GET"])
def deliveries_handler():

    send_date = request.args.get('send_date')
    delivery_date = request.args.get('delivery_date')
    weight_lower = request.args.get('weight_lower')
    weight_upper = request.args.get('weight_upper')
    status = request.args.get('status')

    user_id = 1 # session

    deliveries, response_status = query.get_user_deliveries( user_id, { 'send_date': send_date,
                                              'delivery_date': delivery_date,
                                              'weight_lower': weight_lower,
                                              'weight_upper': weight_upper,
                                              'status': status } )
    if (response_status == 400):
        return "<h1>Некорректный запрос</h1>", 400

    search_options = [ { 'name': "Дата отправки", 'params': None, 'arg': 'send_date' }, 
                       { 'name': "Дата доставки", 'params': None, 'arg': 'delivery_date' },
                       { 'name': "Вес (от)", 'params': None, 'arg': 'weight_lower' },
                       { 'name': "Вес (до)", 'params': None, 'arg': 'weight_upper' },
                       { 'name': "Статус", 'params': ["Завершен", "В работе", "Отменен"], 'arg': 'status' } ]
    
    return render_template('deliveries.html', all=True, deliveries=deliveries, search_options=search_options), 200


# @deliveries_app.route('/<int:delivery_id>')
# def delivey_handler(delivery_id):
#     return render_template('deliveries.html', all=False)


# @deliveries_app.route('/new', methods=["GET", "POST"])
# def new_delivery_handler():
#     return render_template('new-delivery.html')