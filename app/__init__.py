import os

import eventlet
from celery import Celery
from flask import Flask
from flask_admin import Admin
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from redis import Redis

eventlet.monkey_patch()

app = Flask(__name__)

admin = Admin(app)

app.config.from_object(os.environ['APP_SETTINGS'])

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# remove broker?
socketio = SocketIO(app, message_queue=app.config['CELERY_BROKER_URL'])

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
redis = Redis()

from app import views
from app import models

if __name__ == '__main__':
    socketio.run(app)
