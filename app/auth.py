from . import utils
from flask import Blueprint

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/sign_up', methods=['POST'])
def sign_up():
    return utils.sign_up()


@auth_bp.route('/change_password', methods=['PUT'])
def change_password():
    return utils.change_password()
