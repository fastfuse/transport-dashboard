import os


class Config:
    BASEDIR = os.path.abspath(os.path.dirname(__file__))

    MQTT_BROKERS = {
        "HIVE": "broker.hivemq.com",
        "MOSQUITTO": "test.mosquitto.org",
    }

    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY',
                                '(#\x94k\xd9W\xf0\x9f\x9cj\xe8\x1c\xfd\xa2\xcd\x94)B\xe2H\xca\x118\x1a')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
                                             "postgresql://lviv_pt:admin@localhost/lviv_pt_db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL',
                                           'redis://localhost:6379/0')

    CELERY_IMPORTS = ("application.tasks",)


class DevelopmentConfig(Config):
    DEBUG = True


class StagingConfig(Config):
    DEBUG = False


class ProductionConfig(Config):
    DEBUG = False
