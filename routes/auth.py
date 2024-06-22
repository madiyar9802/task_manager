from logic import auth_logic
from flask import Blueprint

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def application_check():
    return "200"


@auth_bp.route('/sign_up', methods=['POST'])
def sign_up():
    return auth_logic.sign_up()


@auth_bp.route('/change_password', methods=['PUT'])
def change_password():
    return auth_logic.change_password()
