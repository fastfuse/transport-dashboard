import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY',
                                '(#\x94k\xd9W\xf0\x9f\x9cj\xe8\x1c\xfd\xa2\xcd\x94)B\xe2H\xca\x118\x1a')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', "postgresql://lviv_pt:admin@localhost/lviv_pt_db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'


class DevelopmentConfig(Config):
    DEBUG = True


class TestConfig(Config):
    DEBUG = True


class StagingConfig(Config):
    DEBUG = False


class ProductionConfig(Config):
    DEBUG = False
