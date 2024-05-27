from flask import request, Response
from models import Executor
from functools import wraps

def check_auth(login, password):
    user = Executor.query.filter_by(login=login).first()
    if user and user.password == password:
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
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return func(*args, **kwargs)

    return decorated
