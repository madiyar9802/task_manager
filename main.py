import models
from config import *
from flask import Flask, jsonify, request

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{user}:{password}@{host}/{dbname}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

models.db.init_app(app)


@app.route('/')
def application_check():
    return "200"


@app.route('/project=<int:project_id>')
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


@app.route('/project=<int:project_id>/task=<int:task_id>')
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
