### Lviv Public Transport Dashboard

#### Development:
* export FLASK_APP=app/__init__.py
* export FLASK_DEBUG=1
* export APP_SETTINGS=config.DevelopmentConfig
* redis-server
* celery worker -A app.celery --loglevel=info
