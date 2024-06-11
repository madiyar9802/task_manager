from app import logic
from flask import Blueprint, current_app

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/sign_up', methods=['POST'])
def sign_up():
    current_app.logger.info("New account has been created")
    return logic.sign_up()


@auth_bp.route('/change_password', methods=['PUT'])
def change_password():
    current_app.logger.info("Password has been changed")
    return logic.change_password()
