from flask import Blueprint, current_app
from app import logic
from app.basic_auth import requires_auth

task_bp = Blueprint('task', __name__)


@task_bp.route('/get_tasks')
@requires_auth
def get_tasks():
    current_app.logger.info("All tasks have been requested")
    return logic.get_tasks()


@task_bp.route('/get_task/<int:task_id>')
@requires_auth
def get_task_id(task_id):
    current_app.logger.info(f"Task {task_id} has been requested")
    return logic.get_task_id(task_id)


@task_bp.route('/create_task', methods=['POST'])
@requires_auth
def create_task():
    current_app.logger.info("New task has been created")
    return logic.create_task()


@task_bp.route('/update_task/<int:task_id>', methods=['PUT'])
@requires_auth
def update_task(task_id):
    current_app.logger.info(f"Task {task_id} has been updated")
    return logic.update_task(task_id)


@task_bp.route('/task/<int:task_id>/create_comment', methods=['POST'])
@requires_auth
def create_comment(task_id):
    current_app.logger.info(f"A new comment has been created for task {task_id}")
    return logic.create_comment(task_id)


@task_bp.route('/task/<int:task_id>/update_comment/<int:comment_id>', methods=['PUT'])
@requires_auth
def update_comment(task_id, comment_id):
    current_app.logger.info(f"Comment {comment_id} for task {task_id} has been updated")
    return logic.update_comment(task_id, comment_id)


@task_bp.route('/task/<int:task_id>/delete_comment/<int:comment_id>', methods=['DELETE'])
@requires_auth
def delete_comment(task_id, comment_id):
    current_app.logger.info(f"Comment {comment_id} for task {task_id} has been deleted")
    return logic.delete_comment(task_id, comment_id)
