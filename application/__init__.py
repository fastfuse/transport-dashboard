import logging
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

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

# Login
login = LoginManager(app)
login.login_view = 'login'

# Admin
admin = Admin(app)

# Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# SocketIO
# TODO: remove - it is not necessary anymore
socketio = SocketIO(app, message_queue=app.config['CELERY_BROKER_URL'])

# Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Redis
redis = r.from_url(app.config['REDIS_URL'])

from application import models

from .admin import admin_blueprint
from .auth import auth_blueprint
from .dashboard import dashboard_blueprint
from .api import api_blueprint

app.register_blueprint(admin_blueprint)
app.register_blueprint(auth_blueprint)
app.register_blueprint(dashboard_blueprint)
app.register_blueprint(api_blueprint)

if __name__ == '__main__':
    socketio.run(app)
