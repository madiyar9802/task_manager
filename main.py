from config import DB_CONFIG
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['dbname']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text)


class Status(db.Model):
    __tablename__ = 'status'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.Text)


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)
    description = db.Column(db.Text)

    project = db.relationship("Project", backref="tasks")
    status = db.relationship("Status", backref="tasks")


class Executor(db.Model):
    __tablename__ = 'executors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    login = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)


class TaskExecutor(db.Model):
    __tablename__ = 'task_executors'

    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), primary_key=True)
    executor_id = db.Column(db.Integer, db.ForeignKey('executors.id'), primary_key=True)


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)


class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    path = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)


@app.route('/api/get_info')
def get_info():
    project = Project.query.all()
    return render_template('index.html', projects=project)


# @app.route('/api/post_task')
# def post_task():
#     return 'post task'
#
#
# @app.route('/api/put_task')
# def put_task():
#     return 'put task'
#
#
# @app.route('/api/delete_task')
# def delete_task():
#     return 'delete task'


if __name__ == '__main__':
    app.run(debug=True)
