from app import models
from schemas import validation_schemas as schemas
from pydantic import ValidationError
from flask import jsonify, g
from sqlalchemy.orm import joinedload


def get_tasks():
    tasks = (
        models.db.session.query(models.Task).join(models.Executor).filter(models.Executor.login == g.username).all()
    )

    if not tasks:
        return jsonify({'error': 'No tasks found for user'}), 404

    all_tasks_data = [
        {
            'id': task.id,
            'project_id': task.project_id,
            'description': task.description,
            'start_time': task.start_time.strftime('%Y-%m-%d %H:%M:%S') if task.start_time else None,
            'end_time': task.end_time.strftime('%Y-%m-%d %H:%M:%S') if task.end_time else None,
            'executor_id': task.executor_id,
            'status_id': task.status_id
        }
        for task in tasks
    ]

    return jsonify(all_tasks_data)


def get_task_id(task_id):
    task = (models.db.session.query(models.Task)
            .join(models.Executor)
            .filter(models.Executor.login == g.username, models.Task.id == task_id)
            .options(joinedload(models.Task.comments))
            .first())

    if not task:
        return jsonify({'error': 'У пользователя нет такой задачи'}), 404

    comment_text = [comment.comment for comment in task.comments]

    task_data = {
        'id': task.id,
        'project_id': task.project_id,
        'description': task.description,
        'start_time': task.start_time.strftime('%Y-%m-%d %H:%M:%S') if task.start_time else None,
        'end_time': task.end_time.strftime('%Y-%m-%d %H:%M:%S') if task.end_time else None,
        'executor_id': task.executor_id,
        'status_id': task.status_id,
        'comments': comment_text
    }
    return jsonify(task_data)


def create_task():
    try:
        data = schemas.CreateTask.parse_obj(g.data)
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400

    executor = models.Executor.query.filter_by(login=g.username).first()
    new_task = models.Task(
        project_id=data.project_id,
        description=data.description,
        start_time=data.start_time,
        end_time=data.end_time,
        executor_id=executor.id,
        status_id=data.status_id
    )
    models.db.session.add(new_task)
    models.db.session.commit()
    return jsonify({'message': 'Задача успешно создана'}), 201


def update_task(task_id):
    task = models.db.session.query(models.Task).join(models.Executor).filter(models.Executor.login == g.username,
                                                                             models.Task.id == task_id).first()

    if task is None:
        return jsonify({'error': 'Задача не найдена'}), 404

    try:
        data = schemas.UpdateTask.parse_obj(g.data)
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400

    task.project_id = data.project_id if data.project_id is not None else task.project_id
    task.status_id = data.status_id if data.status_id is not None else task.status_id
    task.description = data.description if data.description is not None else task.description
    task.start_time = data.start_time if data.start_time is not None else task.start_time
    task.end_time = data.end_time if data.end_time is not None else task.end_time
    models.db.session.commit()

    return jsonify({'message': 'Задача успешно обновлена'})
