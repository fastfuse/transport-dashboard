import os

from flask import Flask
from flask_admin import Admin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from celery import Celery
from flask_socketio import SocketIO

app = Flask(__name__)

admin = Admin(app)

app.config.from_object(os.environ['APP_SETTINGS'])

db = SQLAlchemy(app)
migrate = Migrate(app, db)

socketio = SocketIO(app)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

from app import views
from app import models

if __name__ == '__main__':
    socketio.run(app)
