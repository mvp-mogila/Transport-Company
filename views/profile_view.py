from flask import Blueprint, request, render_template

from wrappers.access_control import login_required
import managers.user_manager as user

profile_app = Blueprint('profile_app', __name__, template_folder="templates")

@login_required
@profile_app.route('/', methods = ['GET'])
def profile_handler():
    user_id = 1
    user_group = ''
    user_info = user.get_user_info(user_id, user_group)
    return render_template('profile.html'), 200