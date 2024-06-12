from flask import Blueprint, current_app, g
from logic import tasks_logic
from app.basic_auth import requires_auth

task_bp = Blueprint('task', __name__)


@task_bp.route('/get_tasks')
@requires_auth
def get_tasks():
    current_app.logger.info(f"All tasks requested by user: {g.username}")
    return tasks_logic.get_tasks()


@task_bp.route('/get_task/<int:task_id>')
@requires_auth
def get_task_id(task_id):
    current_app.logger.info(f"Task {task_id} was requested by user: {g.username}")
    return tasks_logic.get_task_id(task_id)


@task_bp.route('/create_task', methods=['POST'])
@requires_auth
def create_task():
    current_app.logger.info(f"New task was created by user: {g.username}")
    return tasks_logic.create_task()


@task_bp.route('/update_task/<int:task_id>', methods=['PUT'])
@requires_auth
def update_task(task_id):
    current_app.logger.info(f"Task {task_id} was updated by user: {g.username}")
    return tasks_logic.update_task(task_id)
