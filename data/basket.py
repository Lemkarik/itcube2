import sqlalchemy
from app import db
from sqlalchemy import orm


class Basket(db.Model):
    __tablename__ = 'baskets'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.id"), nullable=False)
    adverts_ids = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user = orm.relation('User')
