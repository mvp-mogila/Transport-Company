from flask import Blueprint, request, render_template

from services.access_control import group_required


report_app = Blueprint('report_app', __name__, template_folder='templates')


@group_required
@report_app.route('/check', methods=['GET'])
def report_check_handler():
    return render_template()


@group_required
@report_app.route('/create', methods=['GET', 'POST'])
def report_create_handler():
    return render_template()