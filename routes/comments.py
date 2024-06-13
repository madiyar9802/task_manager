from flask import Blueprint, current_app, g
from logic import comments_logic
from app.basic_auth import requires_auth

comment_bp = Blueprint('comment', __name__)


@comment_bp.route('/task/<int:task_id>/create_comment', methods=['POST'])
@requires_auth
def create_comment(task_id):
    current_app.logger.info(f"A new comment has been created for task {task_id}")
    return comments_logic.create_comment(task_id)


@comment_bp.route('/task/<int:task_id>/update_comment/<int:comment_id>', methods=['PUT'])
@requires_auth
def update_comment(task_id, comment_id):
    current_app.logger.info(f"Comment {comment_id} for task {task_id} was updated")
    return comments_logic.update_comment(task_id, comment_id)


@comment_bp.route('/task/<int:task_id>/delete_comment/<int:comment_id>', methods=['DELETE'])
@requires_auth
def delete_comment(task_id, comment_id):
    current_app.logger.info(f"Comment {comment_id} for task {task_id} was deleted")
    return comments_logic.delete_comment(task_id, comment_id)
