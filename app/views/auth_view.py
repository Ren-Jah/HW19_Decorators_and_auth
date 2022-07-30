from flask_restx import Resource, Namespace
from flask import request, abort
from app.dao.models.user import User
from app.database import db
from app.utils import get_hash, generate_tokens, decode_token

auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthView(Resource):
    def post(self):
        req_json = request.json

        # Проверяем, что оба поля не пустые.
        username = req_json.get("username", None)
        password = req_json.get("password", None)
        if None in [username, password]:
            abort(400)

        # Проверяем, что пользователь существует в Базе.
        user = db.session.query(User).filter(User.username == username).first()
        if user is None:
            return {"error": "Неверные учётные данные"}, 401

        # Получаем хэш пароля пользователя.
        req_json["password"] = get_hash(password)
        password_hash = req_json["password"]

        # Проверяем, что хэши пароля пользователя из базы и при авторизации совпадают.
        if password_hash != user.password:
            return {"error": "Неверные учётные данные"}, 401

        # Генерируем токены.
        data = {
            "username": user.username,
            "role": user.role
        }

        return generate_tokens(data), 201

    def put(self):
        req_json = request.json

        refresh_token = req_json.get("refresh_token")
        if refresh_token is None:
            abort(400)

        decoded_token = decode_token(refresh_token)

        username = decoded_token["username"]
        user = db.session.query(User).filter(User.username == username).first()
        if user is None:
            return {"error": "Неверные учётные данные"}, 401

        data = {
            "username": user.username,
            "role": user.role
        }

        return generate_tokens(data), 201
