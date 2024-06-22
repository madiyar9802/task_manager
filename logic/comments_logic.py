from app import models
from schemas import validation_schemas as schemas
from pydantic import ValidationError
from flask import jsonify, g


def create_comment(task_id):
    try:
        data = schemas.CreateComment.parse_obj(g.data)
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400

    task = (models.db.session.query(models.Task)
            .join(models.Executor)
            .filter(models.Executor.login == g.username, models.Task.id == task_id)
            .first())

    if not task:
        return jsonify({'error': 'У пользователя нет такой задачи'}), 404

    new_comment = models.Comment(
        task_id=task_id,
        comment=data.comment_text
    )
    models.db.session.add(new_comment)
    models.db.session.commit()

    return jsonify({'message': 'Комментарий успешно создан'}), 201


def update_comment(task_id, comment_id):
    try:
        data = schemas.UpdateComment.parse_obj(g.data)
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400

    comment = (models.db.session.query(models.Comment)
               .join(models.Task)
               .join(models.Executor)
               .filter(models.Executor.login == g.username, models.Task.id == task_id, models.Comment.id
                       == comment_id)
               .first())

    if not comment:
        return jsonify({'error': 'Задачи, либо комментария с таким id не существует'}), 404

    comment.comment = data.comment_text if data.comment_text else comment.comment
    comment.task_id = data.task_id if data.task_id else comment.task_id
    models.db.session.commit()

    return jsonify({'message': 'Комментарий успешно изменен'}), 201


def delete_comment(task_id, comment_id):
    comment = (models.db.session.query(models.Comment)
               .join(models.Task)
               .join(models.Executor)
               .filter(models.Executor.login == g.username, models.Task.id == task_id, models.Comment.id
                       == comment_id)
               .first())

    if not comment:
        return jsonify({'error': 'Задачи, либо комментария с таким id не существует'}), 404

    models.db.session.delete(comment)
    models.db.session.commit()

    return jsonify({'message': 'Комментарий успешно удален'}), 200
