from flask import Blueprint, request, render_template, session

from wrappers.access_control import login_required
import managers.delivery_manager as delivery
# import managers.user_manager as user
# import managers.transport_manager as transport


deliveries_app = Blueprint('deliveries_app', __name__, template_folder="templates")


@deliveries_app.route('/', methods=["GET"])
@login_required
def deliveries_handler():
    weight_lower = request.args.get('weight_lower')
    weight_upper = request.args.get('weight_upper')
    status = request.args.get('status')

    user_id = session.get('user_id')

    deliveries, response_status = delivery.get_user_deliveries(user_id, 
                                            {'weight_lower': weight_lower,
                                              'weight_upper': weight_upper,
                                              'status': status})
    if (response_status == 400):
        return "<center><h1>Некорректный запрос</h1></center>", response_status

    search_options = [{'name': "Вес (от)", 'params': None, 'arg': 'weight_lower'},
                      {'name': "Вес (до)", 'params': None, 'arg': 'weight_upper'},
                      {'name': "Статус", 'params': ["Завершен", "В работе", "Отменен"], 'arg': 'status'}]

    return render_template('deliveries.html', all=True, user_deliveries=deliveries, 
                           search_options=search_options, return_page_url='/', staff=False, logged=True), response_status


# @login_required
# @deliveries_app.route('/<int:delivery_id>')
# def delivery_handler(delivery_id):
#     user_id = 1  # session

#     delivery_details, response_status = delivery.get_delivery_info(
#         delivery_id, user_id)

#     if (response_status == 400):
#         return "<center><h1>Некорректный запрос</h1></center>", response_status

#     # if (response_status == 200):
#     #     client_info = user.get_user_fullname(user_id)
#     #     manager_info = user.get_user_fullname(delivery_datils[''])
#     #     driver_info = user.get_user_fullname(delivery_datils[''])
#     #     transport_info = transport.get_transport_info(delivery_dateils[''])

#     return render_template('deliveries.html', all=False, delivery=delivery_details, 
#                            client=client_info, driver=driver_info, manager=manager_info, 
#                            transport=transport_info, return_page_url='/delivery/'), response_status

# @login_required
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
