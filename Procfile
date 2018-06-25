worker_web: gunicorn --worker-class eventlet -w 1 application:app
worker_celery: celery -A application.celery worker --loglevel=info --concurrency=1
worker_publisher: python publisher.py --concurrency=1