from http.client import BAD_REQUEST, CONFLICT, CREATED, NO_CONTENT, NOT_FOUND, OK, UNPROCESSABLE_ENTITY
from flask import Blueprint, request, render_template
from werkzeug.exceptions import BadRequest

from services.access_control import group_required
from managers import report_manager as report

report_app = Blueprint('report_app', __name__, template_folder='templates')


@report_app.route('/check', methods=['GET'])
@group_required
def report_check_handler():

    cargo_name = request.args.get('cargo_name')
    date = request.args.get('date')

    params = {'cargo_name': cargo_name, 'date': date}

    reports, response_code = report.report_info(params)

    errtitle = None
    if (response_code ==  BAD_REQUEST):
        raise BadRequest
    elif (response_code == NOT_FOUND):
        errtitle = "По данному запросу отчетов нет"
    
    form_method = "GET"
    button_title = "Поиск"
    search_options = [ {'name': "Груз", 'params': [{"name": "Малая коробка", "value": "Малая коробка"},
                                                   {"name": "Средняя коробка", "value": "Средняя коробка"},
                                                   {"name": "Большая коробка", "value": "Большая коробка"},
                                                   {"name": "Крупный груз", "value": "Крупный груз"},
                                                   {"name": "Насыпной груз", "value": "Насыпной груз"}],'arg': 'cargo_name', 'type': None},
                {'name': "Промежуток создания отчета", 'params': None, 'arg': 'date', 'type': 'month'} ]

    return render_template('report.html', reports=reports, create=False, errtitle=errtitle,
        form_method=form_method, button_title=button_title, options=search_options,
        logged=True, staff_status=True, return_url='/')


@report_app.route('/create', methods=['GET', 'POST'])
@group_required
def report_create_handler():
    errtitle = None
    form_method = "POST"
    button_title = "Создать"
    search_options = [ {'name': "Груз", 'params': [{"name": "Малая коробка", "value": "Малая коробка"},
                                                   {"name": "Средняя коробка", "value": "Средняя коробка"},
                                                   {"name": "Большая коробка", "value": "Большая коробка"},
                                                   {"name": "Крупный груз", "value": "Крупный груз"},
                                                   {"name": "Насыпной груз", "value": "Насыпной груз"}],'arg': 'cargo_name', 'type': None},
                {'name': "Промежуток создания отчета", 'params': None, 'arg': 'date', 'type': 'month'} ]
    response_code = OK
    if (request.method == 'POST'):
        cargo_name = request.form.get('cargo_name')
        date = request.form.get('date')

        params = {'cargo_name': cargo_name, 'date': date}
        response_code = report.create_report(params)
    
        if (response_code == BAD_REQUEST):
            raise BadRequest
        elif (response_code == CONFLICT):
            errtitle = "Такой отчет уже существует"
        elif (response_code == NO_CONTENT):
            errtitle = "Этот продукт не продавался в указанный период"
        elif (response_code ==  UNPROCESSABLE_ENTITY):
            errtitle = "Указаны не все парметры"
        elif (response_code == CREATED):
            errtitle = "Отчет успешно создан"

    return render_template('report.html', create=True, errtitle = errtitle,
        form_method=form_method, button_title=button_title, options=search_options,
        logged=True, staff_status=True, return_url='/staff/report/check')