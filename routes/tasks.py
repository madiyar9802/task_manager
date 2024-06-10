from flask import Blueprint, current_app
from app import logic
from app.basic_auth import requires_auth

task_bp = Blueprint('task', __name__)


@task_bp.route('/get_tasks')
@requires_auth
def get_tasks():
    current_app.logger.info("Запрошены все задачи")
    return logic.get_tasks()


@task_bp.route('/get_task/<int:task_id>')
@requires_auth
def get_task_id(task_id):
    current_app.logger.info(f"Запрошена задача {task_id}")
    return logic.get_task_id(task_id)


@task_bp.route('/create_task', methods=['POST'])
@requires_auth
def create_task():
    current_app.logger.info("Создана новая задача")
    return logic.create_task()


@task_bp.route('/update_task/<int:task_id>', methods=['PUT'])
@requires_auth
def update_task(task_id):
    current_app.logger.info(f"Задача {task_id} обновлена")
    return logic.update_task(task_id)


@task_bp.route('/task/<int:task_id>/create_comment', methods=['POST'])
@requires_auth
def create_comment(task_id):
    current_app.logger.info(f"Создан новый комментарий для задачи {task_id}")
    return logic.create_comment(task_id)


@task_bp.route('/task/<int:task_id>/update_comment/<int:comment_id>', methods=['PUT'])
@requires_auth
def update_comment(task_id, comment_id):
    current_app.logger.info(f"Комментарий {comment_id} для задачи {task_id} обновлен")
    return logic.update_comment(task_id, comment_id)


@task_bp.route('/task/<int:task_id>/delete_comment/<int:comment_id>', methods=['DELETE'])
@requires_auth
def delete_comment(task_id, comment_id):
    current_app.logger.info(f"Комментарий {comment_id} для задачи {task_id} удален")
    return logic.delete_comment(task_id, comment_id)
