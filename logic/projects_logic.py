from app import models
from schemas import validation_schemas as schemas
from pydantic import ValidationError
from flask import jsonify, g


def get_projects():
    projects = models.db.session.query(models.Project).join(models.Task).join(models.Executor).filter(
        models.Executor.login == g.username).all()

    if not projects:
        return jsonify({'error': 'У пользователя нет проектов'}), 404

    projects_data = [
        {
            'id': project.id,
            'name': project.name,
            'description': project.description,
            'start_time': project.start_time.strftime('%Y-%m-%d %H:%M:%S') if project.start_time else None,
            'end_time': project.end_time.strftime('%Y-%m-%d %H:%M:%S') if project.end_time else None
        }
        for project in projects
    ]

    return jsonify(projects_data)


def get_project_id(project_id):
    project = models.db.session.query(models.Project).join(models.Task).join(models.Executor).filter(
        models.Executor.login == g.username, models.Project.id == project_id).first()

    if not project:
        return jsonify({'error': 'У пользователя нет такого проекта'}), 404

    project_data = {
        'id': project.id,
        'name': project.name,
        'description': project.description,
        'start_time': project.start_time.strftime('%Y-%m-%d %H:%M:%S'),
        'end_time': project.end_time.strftime('%Y-%m-%d %H:%M:%S')
    }
    return jsonify(project_data)


def create_project():
    try:
        data = schemas.CreateProject.parse_obj(g.data)
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
    return jsonify({'message': f'Проект успешно создан, ID проекта - {new_project.id}'}), 201


def update_project(project_id):
    try:
        data = schemas.UpdateProject.parse_obj(g.data)
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400

    project = models.Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Проект не найден'}), 404

    project.name = data.name if data.name else project.name
    project.description = data.description if data.description else project.description
    project.start_time = data.start_time if data.start_time else project.start_time
    project.end_time = data.end_time if data.end_time else project.end_time
    models.db.session.commit()

    return jsonify({'message': 'Проект успешно обновлен'})
