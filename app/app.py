import os
import yaml
import logging.config

from . import models
from flask import Flask, request, g
from routes.auth import auth_bp
from routes.projects import project_bp
from routes.tasks import task_bp
from routes.comments import comment_bp
from error_handlers.error_handlers import register_error_handlers
from dotenv import load_dotenv
from config import config

# Загрузка переменных окружения из .env файла
load_dotenv()

# Создание и конфигурация Flask приложения
app = Flask(__name__)
config_name = os.getenv('FLASK_CONFIG', 'development')
app.config.from_object(config.app_config[config_name])

# Инициализация базы данных с приложением
models.db.init_app(app)

# Открываем конфигурационный файл для логирования в формате .yaml
with open('config/log_config.yaml', 'r') as file:
    log_config = yaml.safe_load(file)

# Настройка логирования с использованием конфигурации из .yaml файла
logging.config.dictConfig(log_config)
logger = logging.getLogger('app')


# Перед каждым запросом собираем информацию о пользователе и запросе, а затем записываем её в лог
@app.before_request
def get_auth_data():
    auth = request.authorization
    if auth:
        g.username = auth.username
        g.password = auth.password
    else:
        g.username = 'Unknown'
        g.password = None

    if request.content_type == 'application/json':
        g.data = request.get_json(silent=True)
    else:
        g.data = None

    logger.info(f"[{request.remote_addr}] {g.username} requested {request.url}")


# Регистрация всех маршрутов (blueprints)
app.register_blueprint(auth_bp)
app.register_blueprint(project_bp, url_prefix='/projects')
app.register_blueprint(task_bp, url_prefix='/tasks')
app.register_blueprint(comment_bp, url_prefix='/task')

# Регистрация обработчиков ошибок
register_error_handlers(app)

if __name__ == '__main__':
    app.run()
