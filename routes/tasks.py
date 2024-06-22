from flask import Blueprint
from logic import tasks_logic
from app.basic_auth import requires_auth

task_bp = Blueprint('task', __name__)


@task_bp.route('/')
@requires_auth
def get_tasks():
    return tasks_logic.get_tasks()


@task_bp.route('/<int:task_id>')
@requires_auth
def get_task_id(task_id):
    return tasks_logic.get_task_id(task_id)


@task_bp.route('/create', methods=['POST'])
@requires_auth
def create_task():
    return tasks_logic.create_task()


@task_bp.route('/update/<int:task_id>', methods=['PUT'])
@requires_auth
def update_task(task_id):
    return tasks_logic.update_task(task_id)
