from flask import Blueprint, current_app
from logic import comments_logic
from app.basic_auth import requires_auth

comment_bp = Blueprint('comment', __name__)


@comment_bp.route('/task/<int:task_id>/create_comment', methods=['POST'])
@requires_auth
def create_comment(task_id):
    return comments_logic.create_comment(task_id)


@comment_bp.route('/task/<int:task_id>/update_comment/<int:comment_id>', methods=['PUT'])
@requires_auth
def update_comment(task_id, comment_id):
    return comments_logic.update_comment(task_id, comment_id)


@comment_bp.route('/task/<int:task_id>/delete_comment/<int:comment_id>', methods=['DELETE'])
@requires_auth
def delete_comment(task_id, comment_id):
    return comments_logic.delete_comment(task_id, comment_id)
