from . import models
from config.config import user, password, host, dbname
from flask import Flask
from routes.auth import auth_bp
from routes.projects import project_bp
from routes.tasks import task_bp
from error_handlers.error_handlers import register_error_handlers

app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{user}:{password}@{host}/{dbname}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

models.db.init_app(app)


@app.route('/')
def application_check():
    return "200"


app.register_blueprint(auth_bp)
app.register_blueprint(project_bp)
app.register_blueprint(task_bp)

register_error_handlers(app)

if __name__ == '__main__':
    app.run(debug=True)
