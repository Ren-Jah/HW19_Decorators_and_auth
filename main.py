from flask import Flask
from flask_restx import Api

from app.config import Config
from app.database import db
from app.views.directors_view import director_ns
from app.views.genres_view import genre_ns
from app.views.movie_view import movies_ns
from app.views.user_view import user_ns
from app.views.auth_view import auth_ns
from app.utils import create_data


def create_app(config: Config):
    application = Flask(__name__)
    application.config.from_object(config)
    application.app_context().push()

    return application


def configure_app(application: Flask):
    db.init_app(application)
    api = Api(app)
    api.add_namespace(movies_ns)
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(user_ns)
    api.add_namespace(auth_ns)
    create_data(app, db)


if __name__ == '__main__':
    app_config = Config()
    app = create_app(app_config)
    configure_app(app)
    app.run(host="localhost", port=7000, debug=True)