from flask import Blueprint, request, render_template

import managers.delivery_manager as delivery
import managers.user_manager as user
import managers.transport_manager as transport


deliveries_app = Blueprint('deliveries_app', __name__, template_folder="templates")


@deliveries_app.route('/', methods=["GET"])
def deliveries_handler():
    send_date = request.args.get('send_date')
    deliv_date = request.args.get('delivery_date')
    weight_lower = request.args.get('weight_lower')
    weight_upper = request.args.get('weight_upper')
    status = request.args.get('status')

    user_id = 1  # session

    deliveries, response_status = delivery.get_user_deliveries(user_id, 
                                            {'send_date': send_date,
                                              'delivery_date': deliv_date,
                                              'weight_lower': weight_lower,
                                              'weight_upper': weight_upper,
                                              'status': status})
    if (response_status == 400):
        return "<center><h1>Некорректный запрос</h1></center>", response_status

    search_options = [{'name': "Дата отправки dd-mm-yyy", 'params': None, 'arg': 'send_date'},
                      {'name': "Дата доставки dd-mm-yyy", 'params': None, 'arg': 'delivery_date'},
                      {'name': "Вес (от)", 'params': None, 'arg': 'weight_lower'},
                      {'name': "Вес (до)", 'params': None, 'arg': 'weight_upper'},
                      {'name': "Статус", 'params': ["Завершен", "В работе", "Отменен", "Отклонен"], 'arg': 'status'}]

    return render_template('deliveries.html', all=True, deliveries=deliveries, 
                           search_options=search_options, return_page_url='/'), response_status


@deliveries_app.route('/<int:delivery_id>')
def delivey_handler(delivery_id):
    user_id = 1  # session

    delivery_details, response_status = delivery.get_delivery_info(
        delivery_id, user_id)

    if (response_status == 400):
        return "<center><h1>Некорректный запрос</h1></center>", response_status

    # if (response_status == 200):
    #     client_info = user.get_user_fullname(user_id)
    #     manager_info = user.get_user_fullname(delivery_datils[''])
    #     driver_info = user.get_user_fullname(delivery_datils[''])
    #     transport_info = transport.get_transport_info(delivery_dateils[''])

    return render_template('deliveries.html', all=False, delivery=delivery_details, 
                           client=client_info, driver=driver_info, manager=manager_info, 
                           transport=transport_info, return_page_url='/delivery/'), response_status


# @deliveries_app.route('/new', methods=["GET", "POST"])
# def new_delivery_handler():
#     if (request.method == 'POST'):
#         send_addr = request.args.get('send_address')
#         deliv_addr = request.args.get('delivery_address')
#         send_date = request.args.get('send_date')
#         deliv_date = request.args.get('delivery_date')
#         items = request.args.getlist('items')

#     # deliveries, response_status = delivery.create_delivery( user_id, { 'send_date': send_date,
#     #                                           'delivery_date': deliv_date,
#     #                                           'weight_lower': weight_lower,
#     #                                           'weight_upper': weight_upper,
#     #                                           'status': status } )

#     return render_template('new-delivery.html', return_page_url='/delivery/')
