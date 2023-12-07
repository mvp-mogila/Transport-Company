from http.client import BAD_REQUEST, NOT_FOUND
from pickletools import optimize
from flask import Blueprint, request, render_template
from werkzeug.exceptions import BadRequest

from services.access_control import group_required
from managers import delivery_manager as delivery

report_app = Blueprint('report_app', __name__, template_folder='templates')


@report_app.route('/check', methods=['GET'])
@group_required
def report_check_handler():

    cargo_name = request.args.get('cargo_name')
    date = request.args.get('date')

    if (date):
        date = date.split('-')
        year = date[0]
        month = date[1]
        params = {'cargo_name': cargo_name, 'year': year, 'month': month}
    else:
        params = {'cargo_name': cargo_name}

    # reports, response_code = delivery.report_info(params)

    # if (response_code ==  BAD_REQUEST):
    #     raise BadRequest

    form_method = "GET"
    button_title = "Поиск"
    search_options = [ {'name': "Груз", 'params': ["Малая коробка", "Средняя коробка", "Большая коробка", "Крупный груз", "Насыпной груз"], 'arg': 'cargo_name', 'type': None},
                {'name': "Промежуток создания отчета", 'params': None, 'arg': 'date', 'type': 'month'} ]

    return render_template('report.html', reports=None, 
        form_method=form_method, button_title=button_title, options=search_options,
        logged=True, staff_status=True, return_url='/')


@report_app.route('/create', methods=['GET', 'POST'])
@group_required
def report_create_handler():
    return render_template()