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
redis = Redis(
    host='redis://h:pe593df26d1d7fdb8665d72c08a142a5ab3c69847a548beeb8b100d7ad66b3ce0@ec2-54-88-234-13.compute-1.amazonaws.com',
    port=25339)

from app import views
from app import models

if __name__ == '__main__':
    socketio.run(app)
