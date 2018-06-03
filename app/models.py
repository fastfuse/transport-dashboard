import uuid

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login

user_stops = db.Table('user_stops',
                      db.Column('user_id', db.Integer,
                                db.ForeignKey('users.id'),
                                primary_key=True),
                      db.Column('stop_id', db.Integer,
                                db.ForeignKey('stops.id'),
                                primary_key=True)
                      )


class Stop(db.Model):
    """
    Model represents Public Transport Stop.
    """

    __tablename__ = "stops"

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    internal_id = db.Column('internal_id', db.String)
    name = db.Column('name', db.Unicode)
    code = db.Column('code', db.String)
    latitude = db.Column('latitude', db.Float)
    longitude = db.Column('longitude', db.Float)


class User(db.Model, UserMixin):
    """
    Model represents User instance.
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column('username', db.String(20), unique=True)
    password_hash = db.Column('password', db.String)
    room = db.Column('room', db.String, default=uuid.uuid4)

    is_admin = db.Column('admin', db.Boolean, default=False)

    stops = db.relationship('Stop', secondary=user_stops, lazy='subquery',
                            backref=db.backref('users', lazy=True))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
