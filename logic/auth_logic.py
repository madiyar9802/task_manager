from app import models
from schemas import validation_schemas as schemas
from pydantic import ValidationError
from flask import jsonify, g
from werkzeug.security import generate_password_hash, check_password_hash


def sign_up():
    try:
        data = schemas.SignUpModel.parse_obj(g.data)
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400

    if models.Executor.query.filter_by(login=data.login).first():
        return jsonify({'error': 'Пользователь уже существует'}), 400

    hashed_password = generate_password_hash(data.password, method='pbkdf2:sha256')
    new_user = models.Executor(name=data.name,
                               surname=data.surname,
                               email=data.email,
                               login=data.login,
                               password=hashed_password)
    models.db.session.add(new_user)
    models.db.session.commit()

    return jsonify({'message': 'Регистрация успешно завершена'}), 201


def change_password():
    try:
        data = schemas.ChangePassword.parse_obj(g.data)
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400

    user = models.Executor.query.filter_by(login=g.username).first()
    if not user or not check_password_hash(user.password, data.old_password):
        return jsonify({'error': 'Старый пароль введен неверно'}), 400

    user.password = generate_password_hash(data.new_password, method='pbkdf2:sha256')
    models.db.session.commit()

    return jsonify({'message': 'Пароль успешно сменен'})
