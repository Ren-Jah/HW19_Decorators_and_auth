from flask_restx import Resource, Namespace
from flask import request, abort
from app.dao.models.user import User, UserSchema
from app.database import db
from app.utils import get_hash

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    def get(self):
        query_all = db.session.query(User).all()

        return UserSchema(many=True).dump(query_all), 200

    def post(self):
        req_json = request.json
        username = req_json.get("username", None)
        password = req_json.get("password", None)
        if None in [username, password]:
            abort(400)

        # заменяем пароль в словаре по пользователю на хэш пароля.
        req_json["password"] = get_hash(password)

        user_ = UserSchema().load(req_json)
        new_user = User(**user_)
        with db.session.begin():
            db.session.add(new_user)
        return "Created", 201



@user_ns.route('/<int:user_id>')
class UserView(Resource):
    def get(self, user_id):
        query_one = db.session.query(User).get(user_id)

        return UserSchema().dump(query_one), 200

    def put(self, user_id):
        user_selected = db.session.query(User).filter(User.id == user_id)
        user_first = user_selected.first()

        if user_first is None:
            return "Not found", 404

        req_json = request.json

        if "password" in req_json:
            # заменяем пароль в словаре по пользователю на хэш пароля.
            req_json["password"] = get_hash(req_json["password"])

        user_selected.update(req_json)
        db.session.commit()
        return "No Content", 204

    def delete(self, user_id):
        user_selected = db.session.query(User).filter(User.id == user_id)
        user_first = user_selected.first()

        if user_first is None:
            return "Not found", 404

        rows_deleted = user_selected.delete()
        # если произошло удаление более 1 строки, то указываем на наличие проблемы.
        if rows_deleted != 1:
            return "Bad request", 400

        db.session.commit()
        return "No Content", 204