import os

import eventlet
import redis as r
from celery import Celery
from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

eventlet.monkey_patch()

app = Flask(__name__)

login = LoginManager(app)
login.login_view = 'login'

admin = Admin(app)

app.config.from_object(os.environ['APP_SETTINGS'])

db = SQLAlchemy(app)
migrate = Migrate(app, db)

socketio = SocketIO(app, message_queue=app.config['CELERY_BROKER_URL'])

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

redis = r.from_url(app.config['REDIS_URL'])

from app import views
from app import models

if __name__ == '__main__':
    socketio.run(app)
