import flask
from flask import request, Response
from flask_restx import Namespace, Resource

from app.dao.models.movie import MovieSchema, Movie
from app.database import db
from app.utils import auth_required, admin_required

movies_ns = Namespace('movies')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movies_ns.route("/")
class MoviesView(Resource):
    @auth_required
    def get(self):
        all_movies_query = db.session.query(Movie)

        director_id = request.args.get("director_id")
        if director_id:
            all_movies_query = all_movies_query.filter(Movie.director_id == director_id)

        genre_id = request.args.get("genre_id")
        if genre_id:
            all_movies_query = all_movies_query.filter(Movie.genre_id == genre_id)

        year_selected = request.args.get("year")
        if year_selected:
            all_movies_query = all_movies_query.filter(Movie.year == year_selected)

        final_query = all_movies_query.all()

        if len(final_query) >= 1:
            return movies_schema.dump(final_query), 200
        else:
            return f"Таких фильмов нет"

    @admin_required
    def post(self):
        new_data = request.json

        movie = movie_schema.load(new_data)
        new_movie = Movie(**movie)
        with db.session.begin():
            db.session.add(new_movie)

        return "Created", 201


# Вьюшка отображает полную информацию по фильму по выбранному id
@movies_ns.route("/<int:mid>")
class MovieView(Resource):
    @auth_required
    def get(self, mid):
        try:
            movie = Movie.query.get_or_404(mid)
            return movie_schema.dump(movie), 200

        except KeyError:
            return flask.json.dumps(Response)

    @admin_required
    def put(self, mid):
        movie_selected = db.session.query(Movie).filter(Movie.id == mid)
        movie_first = movie_selected.first()

        if movie_first is None:
            return "Not found", 404

        new_data = request.json
        movie_selected.update(new_data)
        db.session.commit()

        return "No Content", 204

    @admin_required
    def delete(self, mid):
        movie_selected = db.session.query(Movie).filter(Movie.id == mid)
        movie_first = movie_selected.first()

        if movie_first is None:
            return "Not found", 404

        rows_deleted = movie_selected.delete()

        # если произошло удаление более 1 строки, то указываем на наличие проблемы.
        if rows_deleted != 1:
            return "Bad request", 400

        db.session.commit()
        return "No Content", 204