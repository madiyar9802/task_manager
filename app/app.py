from . import models
from config.config import user, password, host, dbname
from flask import Flask
from .auth import auth_bp
from .projects import project_bp
from .tasks import task_bp

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

if __name__ == '__main__':
    app.run(debug=True)
