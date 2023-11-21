from flask import Blueprint, render_template

import client_query.delivery_manager as query

deliveries_app = Blueprint('deliveries_app', __name__, template_folder = "templates")


@deliveries_app.route('/deliveries', methods=["GET"])
def deliveries_handler():
    deliveries = query.all_user_deliveries(1)
    return render_template('deliveries.html', all = True, deliveries = deliveries)


@deliveries_app.route('/<int:delivery_id>')
def delivey_handler(delivery_id):
    return render_template('deliveries.html', all = False)


# @deliveries_app.route('/new-delivery', methods=["GET", "POST"])
# def new_delivery_handler():
#     return render_template('new-delivery.html')