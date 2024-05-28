import models
from config import *
from flask import Flask, jsonify, request
from basic_auth import requires_auth
from models import Executor, db
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{user}:{password}@{host}/{dbname}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

models.db.init_app(app)


@app.route('/')
def application_check():
    return "200"


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    surname = data.get('surname')
    email = data.get('email')
    login = data.get('login')
    password = data.get('password')
    if not (name and surname and email and login and password):
        return jsonify({'error': 'Требуется логин и пароль'}), 400
    if Executor.query.filter_by(login=login).first():
        return jsonify({'error': 'Пользователь уже существует'}), 400
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = Executor(name=name, surname=surname, email=email, login=login, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Регистрация успешно завершена'}), 201


@app.route('/change_password', methods=['PUT'])
def change_password():
    auth = request.authorization
    data = request.json
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    if not old_password or not new_password:
        return jsonify({'error': 'Требуется ввести старый и новый пароль'}), 400
    user = Executor.query.filter_by(login=auth.username).first()
    if not (user or check_password_hash(user.password, old_password)):
        return jsonify({'error': 'Старый пароль введен неверно'}), 400
    user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
    db.session.commit()
    return jsonify({'message': 'Пароль успешно сменен'})


@app.route('/project=<int:project_id>')
@requires_auth
def get_project(project_id):
    project = models.Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404

    project_data = {
        'id': project.id,
        'name': project.name,
        'description': project.description,
        'start_time': project.start_time.strftime('%Y-%m-%d %H:%M:%S'),
        'end_time': project.end_time.strftime('%Y-%m-%d %H:%M:%S')
    }
    return jsonify(project_data)


@app.route('/project=<int:project_id>', methods=['PUT'])
@requires_auth
def update_project(project_id):
    project = models.Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found'}), 404
    data = request.json
    project.name = data.get('name', project.name)
    project.description = data.get('description', project.description)
    project.start_time = data.get('start_time', project.start_time)
    project.end_time = data.get('end_time', project.end_time)
    models.db.session.commit()
    return jsonify({'message': 'Project updated successfully'})


@app.route('/project=<int:project_id>/task=<int:task_id>')
@requires_auth
def get_task(project_id, task_id):
    task = models.Task.query.join(models.Project).filter(models.Task.id == task_id,
                                                         models.Project.id == project_id).first()
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    task_data = {
        'id': task.id,
        'project_id': task.project_id,
        'description': task.description,
        'start_time': task.start_time.strftime('%Y-%m-%d %H:%M:%S'),
        'end_time': task.end_time.strftime('%Y-%m-%d %H:%M:%S'),
        'executor_id': task.executor_id,
        'status_id': task.status_id
    }
    return jsonify(task_data)


@app.route('/projects', methods=['POST'])
@requires_auth
def create_project():
    data = request.json
    new_project = models.Project(
        name=data['name'],
        description=data['description'],
        start_time=data['start_time'],
        end_time=data['end_time']
    )
    models.db.session.add(new_project)
    models.db.session.commit()
    return jsonify({'message': 'Project created successfully'}), 201


@app.route('/projects/tasks', methods=['POST'])
@requires_auth
def create_task():
    data = request.json
    new_task = models.Task(
        project_id=data['project_id'],
        description=data['description'],
        start_time=data['start_time'],
        end_time=data['end_time'],
        executor_id=data['executor_id'],
        status_id=data['status_id']
    )
    models.db.session.add(new_task)
    models.db.session.commit()
    return jsonify({'message': 'Task created successfully'}), 201


if __name__ == '__main__':
    app.run(debug=True)
