from flask import Blueprint
from logic import projects_logic
from app.basic_auth import requires_auth

project_bp = Blueprint('project', __name__)


@project_bp.route('/get_projects')
@requires_auth
def get_projects():
    return projects_logic.get_projects()


@project_bp.route('/get_project/<int:project_id>')
@requires_auth
def get_project_id(project_id):
    return projects_logic.get_project_id(project_id)


@project_bp.route('/create_project', methods=['POST'])
@requires_auth
def create_project():
    return projects_logic.create_project()


@project_bp.route('/update_project/<int:project_id>', methods=['PUT'])
@requires_auth
def update_project(project_id):
    return projects_logic.update_project(project_id)
