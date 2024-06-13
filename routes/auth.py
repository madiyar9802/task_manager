from logic import auth_logic
from flask import Blueprint, current_app, g

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/sign_up', methods=['POST'])
def sign_up():
    current_app.logger.info("New user has been created")
    return auth_logic.sign_up()


@auth_bp.route('/change_password', methods=['PUT'])
def change_password():
    current_app.logger.info("Password update successful")
    return auth_logic.change_password()
