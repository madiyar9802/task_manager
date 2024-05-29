import models
from config import user, password, host, dbname
from flask import Flask, jsonify, request
from basic_auth import requires_auth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{user}:{password}@{host}/{dbname}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

models.db.init_app(app)


@app.route('/')
def application_check():
    return "200"


@app.route('/sign_up', methods=['POST'])
def sign_up():
    data = request.json
    name = data.get('name')
    surname = data.get('surname')
    email = data.get('email')
    login = data.get('login')
    password = data.get('password')
    if not (name and surname and email and login and password):
        return jsonify({'error': 'Требуется ввести все данные'}), 400
    if models.Executor.query.filter_by(login=login).first():
        return jsonify({'error': 'Пользователь уже существует'}), 400
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = models.Executor(name=name, surname=surname, email=email, login=login, password=hashed_password)
    models.db.session.add(new_user)
    models.db.session.commit()
    return jsonify({'message': 'Регистрация успешно завершена'}), 201


@app.route('/change_password', methods=['PUT'])
def change_password():
    auth = request.authorization
    data = request.json
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    if not old_password or not new_password:
        return jsonify({'error': 'Требуется ввести старый и новый пароль'}), 400
    user = models.Executor.query.filter_by(login=auth.username).first()
    if not user or not check_password_hash(user.password, old_password):
        return jsonify({'error': 'Старый пароль введен неверно'}), 400
    user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
    models.db.session.commit()
    return jsonify({'message': 'Пароль успешно сменен'})


# PROJECT METHODS
@app.route('/get_projects')
@requires_auth
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


@app.route('/create_project', methods=['POST'])
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


@app.route('/update_project/<int:project_id>', methods=['PUT'])
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


# TASK METHODS
@app.route('/get_tasks')
@requires_auth
def get_task():
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


@app.route('/create_task', methods=['POST'])
@requires_auth
def create_task():
    auth = request.authorization
    data = request.json
    executor = models.Executor.query.filter_by(login=auth.username).first()
    new_task = models.Task(
        project_id=data['project_id'],
        description=data['description'],
        start_time=data['start_time'],
        end_time=data['end_time'],
        executor_id=executor.id,
        status_id=data['status_id']
    )
    models.db.session.add(new_task)
    models.db.session.commit()
    return jsonify({'message': 'Задача успешно создана'}), 201


@app.route('/update_task/<int:task_id>', methods=['PUT'])
@requires_auth
def update_task(task_id):
    auth = request.authorization
    executor = models.Executor.query.filter_by(login=auth.username).first()
    task = models.Task.query.filter_by(executor_id=executor.id).first()
    print(task.id)
    if not task_id == task.id:
        return jsonify({'error': 'Задача не найдена'}), 404
    data = request.json
    task.status_id = data.get('status_id', task.status_id)
    task.description = data.get('description', task.description)
    task.start_time = data.get('start_time', task.start_time)
    task.end_time = data.get('end_time', task.end_time)
    task.executor_id = data.get('executor_id', task.executor_id)
    models.db.session.commit()
    return jsonify({'message': 'Задача успешно обновлена'})


if __name__ == '__main__':
    app.run(debug=True)
