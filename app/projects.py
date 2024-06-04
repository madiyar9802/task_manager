from flask import Blueprint
from . import utils
from .basic_auth import requires_auth

project_bp = Blueprint('project', __name__)


@project_bp.route('/get_projects')
@requires_auth
def get_projects():
    return utils.get_projects()


@project_bp.route('/get_project/<int:project_id>')
@requires_auth
def get_project_id(project_id):
    return utils.get_project_id(project_id)


@project_bp.route('/create_project', methods=['POST'])
@requires_auth
def create_project():
    return utils.create_project()


@project_bp.route('/update_project/<int:project_id>', methods=['PUT'])
@requires_auth
def update_project(project_id):
    return utils.update_project(project_id)
