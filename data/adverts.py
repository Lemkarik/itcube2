from app import db

import sqlalchemy


class Advert(db.Model):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    position = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    seller = sqlalchemy.Column(sqlalchemy.String, nullable=False)
