from flask import Blueprint, current_app, g
from logic import projects_logic
from app.basic_auth import requires_auth

project_bp = Blueprint('project', __name__)


@project_bp.route('/get_projects')
@requires_auth
def get_projects():
    current_app.logger.info(f"All projects requested by user: {g.username}")
    return projects_logic.get_projects()


@project_bp.route('/get_project/<int:project_id>')
@requires_auth
def get_project_id(project_id):
    current_app.logger.info(f"Project {project_id} was requested by user: {g.username}")
    return projects_logic.get_project_id(project_id)


@project_bp.route('/create_project', methods=['POST'])
@requires_auth
def create_project():
    current_app.logger.info(f"New project was created by user: {g.username}")
    return projects_logic.create_project()


@project_bp.route('/update_project/<int:project_id>', methods=['PUT'])
@requires_auth
def update_project(project_id):
    current_app.logger.info(f"Project {project_id} was updated by user: {g.username}")
    return projects_logic.update_project(project_id)
