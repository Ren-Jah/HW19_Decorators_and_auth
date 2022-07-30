from app.database import db
from marshmallow import Schema, fields


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def to_dict(self):
        """Оборачиваем данные жанра в словарь"""
        return {
            "id": self.id,
            "name": self.name
        }


class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()