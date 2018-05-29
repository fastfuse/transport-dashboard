import uuid

from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login
from flask_login import UserMixin


class Stop(db.Model):
    """
    Model represents Public Transport Stop.
    """

    __tablename__ = "stops"

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    internal_id = db.Column('internal_id', db.String)
    name = db.Column('name', db.Unicode)
    code = db.Column('code', db.String)

    # location = db.Column('location', db.String)

    def __init__(self, internal_id, name, code):
        self.internal_id = internal_id
        self.name = name
        self.code = code


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column('username', db.String(20), unique=True)
    password_hash = db.Column('password', db.String)
    room = db.Column('room', db.String, default=uuid.uuid4)

    # def __init__(self, username, password):
    #     self.username = username
    #     self.password_hash = password

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
