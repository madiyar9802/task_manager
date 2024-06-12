from flask import Response, g
from app.models import Executor
from functools import wraps
from werkzeug.security import check_password_hash


def check_auth():
    user = Executor.query.filter_by(login=g.username).first()
    if user and check_password_hash(user.password, g.password):
        return True
    return False


def authenticate():
    return Response(
        'Авторизация не удалась.\n'
        'Вы должны ввести валидные данные', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if not all((g.username, g.password, check_auth())):
            return authenticate()
        return func(*args, **kwargs)

    return decorated
