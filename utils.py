import models
import schemas
from pydantic import ValidationError
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash


def sign_up():
    try:
        data = schemas.SignUpModel.parse_obj(request.json)
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400
    if models.Executor.query.filter_by(login=data.login).first():
        return jsonify({'error': 'Пользователь уже существует'}), 400

    hashed_password = generate_password_hash(data.password, method='pbkdf2:sha256')
    new_user = models.Executor(name=data.name,
                               surname=data.surname,
                               email=data.email,
                               login=data.login,
                               password=hashed_password)
    models.db.session.add(new_user)
    models.db.session.commit()

    return jsonify({'message': 'Регистрация успешно завершена'}), 201


def change_password():
    auth = request.authorization
    try:
        data = schemas.ChangePassword.parse_obj(request.json)
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400

    user = models.Executor.query.filter_by(login=auth.username).first()
    if not user or not check_password_hash(user.password, data.old_password):
        return jsonify({'error': 'Старый пароль введен неверно'}), 400

    user.password = generate_password_hash(data.new_password, method='pbkdf2:sha256')
    models.db.session.commit()

    return jsonify({'message': 'Пароль успешно сменен'})


def get_projects():
    auth = request.authorization
    executor = models.Executor.query.filter_by(login=auth.username).first()
    tasks = models.Task.query.filter_by(executor_id=executor.id).all()

    if not tasks:
        return jsonify({'error': 'У пользователя нет задач и проектов'}), 404

    projects_data = []
    for task in tasks:
        project = models.Project.query.get(task.project_id)
        if project:
            project_data = {
                'id': project.id,
                'name': project.name,
                'description': project.description,
                'start_time': project.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                'end_time': project.end_time.strftime('%Y-%m-%d %H:%M:%S')
            }
            projects_data.append(project_data)

    return jsonify(projects_data)


def get_project_id(project_id):
    auth = request.authorization
    executor = models.Executor.query.filter_by(login=auth.username).first()

    if executor is None:
        return jsonify({'error': 'Пользователь не найден'}), 404

    task = models.Task.query.filter_by(executor_id=executor.id, project_id=project_id).first()
    if task is None:
        return jsonify({'error': 'У пользователя нет такого проекта'}), 404

    project = models.Project.query.get(project_id)
    if project:
        project_data = {
            'id': project.id,
            'name': project.name,
            'description': project.description,
            'start_time': project.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'end_time': project.end_time.strftime('%Y-%m-%d %H:%M:%S')
        }
        return jsonify(project_data)
    return jsonify({'error': 'Проект не найден'}), 404


def create_project():
    try:
        data = schemas.CreateProject.parse_obj(request.json)
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400

    new_project = models.Project(
        name=data.name,
        description=data.description,
        start_time=data.start_time,
        end_time=data.end_time
    )
    models.db.session.add(new_project)
    models.db.session.commit()
    return jsonify({'message': 'Project created successfully'}), 201


def update_project(project_id):
    project = models.Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Проект не найден'}), 404

    try:
        data = schemas.UpdateProject.parse_obj(request.json)
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400

    project.name = data.name if data.name else project.name
    project.description = data.description if data.description else project.description
    project.start_time = data.start_time if data.start_time else project.start_time
    project.end_time = data.end_time if data.end_time else project.end_time
    models.db.session.commit()

    return jsonify({'message': 'Проект успешно обновлен'})


def get_tasks():
    auth = request.authorization
    executor = models.Executor.query.filter_by(login=auth.username).first()
    tasks = models.Task.query.filter_by(executor_id=executor.id).all()
    if not tasks:
        return jsonify({'error': 'У пользователя нет задач'}), 404

    tasks_data = []
    for task in tasks:
        task_data = {
            'id': task.id,
            'project_id': task.project_id,
            'description': task.description,
            'start_time': task.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'end_time': task.end_time.strftime('%Y-%m-%d %H:%M:%S'),
            'executor_id': task.executor_id,
            'status_id': task.status_id
        }
        tasks_data.append(task_data)

    return jsonify(tasks_data)


def get_task_id(task_id):
    auth = request.authorization
    executor = models.Executor.query.filter_by(login=auth.username).first()
    if executor is None:
        return jsonify({'error': 'Пользователь не найден'}), 404

    task = models.Task.query.filter_by(id=task_id, executor_id=executor.id).first()
    if task is None:
        return jsonify({'error': 'У пользователя нет такой задачи'}), 404

    comments = models.Comment.query.filter_by(task_id=task_id).all()
    if comments:
        comment_text = []
        for comment_data in comments:
            comment_text.append(comment_data.comment)
    task_data = {
        'id': task.id,
        'project_id': task.project_id,
        'description': task.description,
        'start_time': task.start_time.strftime('%Y-%m-%d %H:%M:%S'),
        'end_time': task.end_time.strftime('%Y-%m-%d %H:%M:%S'),
        'executor_id': task.executor_id,
        'status_id': task.status_id,
        'comments': comment_text
    }
    return jsonify(task_data)


def create_task():
    auth = request.authorization
    try:
        data = schemas.CreateTask.parse_obj(request.json)
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400

    executor = models.Executor.query.filter_by(login=auth.username).first()
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
    auth = request.authorization
    executor = models.Executor.query.filter_by(login=auth.username).first()
    task = models.Task.query.filter_by(executor_id=executor.id).first()
    if task is None:
        return jsonify({'error': 'Задача не найдена'}), 404

    try:
        data = schemas.UpdateTask.parse_obj(request.json)
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400

    task.project_id = data.project_id if data.project_id is not None else task.project_id
    task.status_id = data.status_id if data.status_id is not None else task.status_id
    task.description = data.description if data.description is not None else task.description
    task.start_time = data.start_time if data.start_time is not None else task.start_time
    task.end_time = data.end_time if data.end_time is not None else task.end_time
    models.db.session.commit()

    return jsonify({'message': 'Задача успешно обновлена'})


def create_comment(task_id):
    auth = request.authorization
    executor = models.Executor.query.filter_by(login=auth.username).first()
    if executor is None:
        return jsonify({'error': 'Пользователь не найден'}), 404

    task = models.Task.query.filter_by(id=task_id, executor_id=executor.id).first()
    if task is None:
        return jsonify({'error': 'У пользователя нет такой задачи'}), 404

    try:
        data = schemas.CreateComment.parse_obj(request.json)
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400

    new_comment = models.Comment(
        task_id=task_id,
        comment=data.comment_text
    )
    models.db.session.add(new_comment)
    models.db.session.commit()

    return jsonify({'message': 'Комментарий успешно создан'}), 201


def update_comment(task_id, comment_id):
    auth = request.authorization
    executor = models.Executor.query.filter_by(login=auth.username).first()
    if executor is None:
        return jsonify({'error': 'Пользователь не найден'}), 404

    task = models.Task.query.filter_by(id=task_id, executor_id=executor.id).first()
    if task is None:
        return jsonify({'error': 'У пользователя нет такой задачи'}), 404

    comment = models.Comment.query.get(comment_id)
    if not comment:
        return jsonify({'error': 'Комментария с таким id не существует'}), 404

    try:
        data = schemas.UpdateComment.parse_obj(request.json)
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400

    comment.comment = data.comment_text if data.comment_text else comment.comment
    comment.task_id = data.task_id if data.task_id else comment.task_id
    models.db.session.commit()

    return jsonify({'message': 'Комментарий успешно изменен'}), 201


def delete_comment(task_id, comment_id):
    auth = request.authorization
    executor = models.Executor.query.filter_by(login=auth.username).first()
    if executor is None:
        return jsonify({'error': 'Пользователь не найден'}), 404

    task = models.Task.query.filter_by(id=task_id, executor_id=executor.id).first()
    if task is None:
        return jsonify({'error': 'У пользователя нет такой задачи'}), 404

    comment = models.Comment.query.filter_by(id=comment_id, task_id=task.id).first()
    if comment is None:
        return jsonify({'error': 'Комментария с таким id не существует'}), 404

    models.db.session.delete(comment)
    models.db.session.commit()

    return jsonify({'message': 'Комментарий успешно удален'}), 200
