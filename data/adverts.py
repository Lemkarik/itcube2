import sqlalchemy
from app import db
from sqlalchemy import orm


class Adverts(db.Model):
    __tablename__ = 'adverts'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    position = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    seller = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.id"), nullable=False)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    user = orm.relation('User')
