import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY',
                                '(#\x94k\xd9W\xf0\x9f\x9cj\xe8\x1c\xfd\xa2\xcd\x94)B\xe2H\xca\x118\x1a')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
                                             "postgresql://lviv_pt:admin@localhost/lviv_pt_db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://h:pe593df26d1d7fdb8665d72c08a142a5ab3c69847a548beeb8b100d7ad66b3ce0@ec2-54-88-234-13.compute-1.amazonaws.com:25339')
    CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL',
                                           'redis://h:pe593df26d1d7fdb8665d72c08a142a5ab3c69847a548beeb8b100d7ad66b3ce0@ec2-54-88-234-13.compute-1.amazonaws.com:25339')


class DevelopmentConfig(Config):
    DEBUG = True


class TestConfig(Config):
    DEBUG = True


class StagingConfig(Config):
    DEBUG = False


class ProductionConfig(Config):
    DEBUG = False
