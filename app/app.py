import logging
import os

from . import models
from flask import Flask, request, g
from routes.auth import auth_bp
from routes.projects import project_bp
from routes.tasks import task_bp
from routes.comments import comment_bp
from error_handlers.error_handlers import register_error_handlers
from dotenv import load_dotenv
from config import config

load_dotenv()

app = Flask(__name__)
config_name = os.getenv('FLASK_CONFIG', 'development')
app.config.from_object(config.app_config[config_name])

models.db.init_app(app)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    handlers=[
                        logging.FileHandler("app.log"),
                        logging.StreamHandler()
                    ])


@app.before_request
def get_auth_data():
    auth = request.authorization
    if auth:
        g.username = auth.username
        g.password = auth.password
    else:
        g.username = None
        g.password = None

    if request.content_type == 'application/json':
        g.data = request.get_json(silent=True)
    else:
        g.data = None


@app.route('/')
def application_check():
    app.logger.debug("Application check endpoint has been reached.")
    return "200"


app.register_blueprint(auth_bp)
app.register_blueprint(project_bp)
app.register_blueprint(task_bp)
app.register_blueprint(comment_bp)

register_error_handlers(app)

if __name__ == '__main__':
    app.run()
