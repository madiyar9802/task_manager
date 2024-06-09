from app import logic
from flask import Blueprint

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/sign_up', methods=['POST'])
def sign_up():
    return logic.sign_up()


@auth_bp.route('/change_password', methods=['PUT'])
def change_password():
    return logic.change_password()
