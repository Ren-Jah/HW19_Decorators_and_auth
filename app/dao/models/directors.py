from app.database import db
from marshmallow import Schema, fields


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    def to_dict(self):
        """Оборачиваем данные режиссера в словарь"""
        return {
            "id": self.id,
            "name": self.name
        }


class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()