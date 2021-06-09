import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = sqlalchemy.Column(db.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(db.String, nullable=False)
    position = sqlalchemy.Column(db.String, nullable=False)
    email = sqlalchemy.Column(db.String, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(db.String, nullable=False)
    role = sqlalchemy.Column(db.Boolean, nullable=False)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)