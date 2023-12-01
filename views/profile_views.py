from flask import Blueprint, request, render_template, session

from wrappers.access_control import login_required
import managers.user_manager as user
import managers.staff_manager as staff

profile_app = Blueprint('profile_app', __name__, template_folder="templates")


@login_required
@profile_app.route('/', methods = ['GET'])
def profile_handler():
    user_id = session.get('user_id')

    user_info = user.user_info(user_id)

    if (user_info['staff_status']):
        staff_info = staff.staff_info(user_id)

    return render_template('profile.html', user=user_info, staff=staff_info), 200