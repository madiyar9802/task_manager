import models
import utils
from config import user, password, host, dbname
from flask import Flask
from basic_auth import requires_auth

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
    return utils.sign_up()


@app.route('/change_password', methods=['PUT'])
def change_password():
    return utils.change_password()


# PROJECT METHODS
@app.route('/get_projects')
@requires_auth
def get_projects():
    return utils.get_projects()


@app.route('/get_project/<int:project_id>')
@requires_auth
def get_project_id(project_id):
    return utils.get_project_id(project_id)


@app.route('/create_project', methods=['POST'])
@requires_auth
def create_project():
    return utils.create_project()


@app.route('/update_project/<int:project_id>', methods=['PUT'])
@requires_auth
def update_project(project_id):
    return utils.update_project(project_id)


# TASK METHODS
@app.route('/get_tasks')
@requires_auth
def get_tasks():
    return utils.get_tasks()


@app.route('/get_task/<int:task_id>')
@requires_auth
def get_task_id(task_id):
    return utils.get_task_id(task_id)


@app.route('/create_task', methods=['POST'])
@requires_auth
def create_task():
    return utils.create_task()


@app.route('/update_task/<int:task_id>', methods=['PUT'])
@requires_auth
def update_task(task_id):
    return utils.update_task(task_id)


# COMMENT METHODS
@app.route('/task/<int:task_id>/create_comment', methods=['POST'])
@requires_auth
def create_comment(task_id):
    return utils.create_comment(task_id)


@app.route('/task/<int:task_id>/update_comment/<int:comment_id>', methods=['PUT'])
@requires_auth
def update_comment(task_id, comment_id):
    return utils.update_comment(task_id, comment_id)


@app.route('/task/<int:task_id>/delete_comment/<int:comment_id>', methods=['DELETE'])
@requires_auth
def delete_comment(task_id, comment_id):
    return utils.delete_comment(task_id, comment_id)


if __name__ == '__main__':
    app.run(debug=True)
