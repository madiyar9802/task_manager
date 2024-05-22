from config import DB_CONFIG
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['dbname']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class tasks_table(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    executor = db.Column(db.String(30), nullable=False)
    status = db.Column(db.String(30), nullable=False)


@app.route('/api/get_task')
def get_task():
    tasks = tasks_table.query.all()
    print(tasks)
    return render_template('index.html', tasks=tasks)


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
    with app.app_context():
        db.create_all()
    app.run(debug=True)
