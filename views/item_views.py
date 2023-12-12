from http.client import FOUND
from math import log
from flask import Blueprint, render_template, request, session, redirect, url_for

from managers import cargo_manager as cargo
from services.access_control import login_required

items_app = Blueprint('items_app', __name__, template_folder="templates")


@items_app.route('/', methods=['GET', 'POST'])
@login_required
def default_order_handler(total_weight = 0):
    if (request.method == 'POST'):
        cargo_id = request.form.get('cargo_id')
        item, response_code = cargo.get_cargo_info(cargo_id)
        print(total_weight)
        if (response_code == FOUND):
            total_weight += add_to_order(cargo_id, item)
            print(total_weight)
            return redirect(url_for('client_app.items_app.default_order_handler', total_weight=total_weight))
    else:
        if (not session.get('items')):
            total_weight = 0
        cargo_list = cargo.get_all_cargos()
        return render_template('cargo-order.html', cargos=cargo_list, logged=True, total_weight=total_weight, order_items=order_items, return_url='/')




@items_app.route('/')
@login_required
def add_to_order(cargo_id, item):
    session.permanent = True
    if cargo_id in session.get('items'):
        session['items'][cargo_id]['amount'] += 1
    else:
        session['items'][cargo_id] = item
        session['items'][cargo_id]['amount'] = 1
    return int(item['weight'])


@items_app.route('/clear')
@login_required
def clear_order():
    session['items'] = {}
    session.modified = True
    return redirect(url_for('client_app.items_app.default_order_index'))
