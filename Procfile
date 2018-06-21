web: gunicorn --worker-class eventlet -w 1 app:app
worker_celery: celery -A app.celery worker --loglevel=info --concurrency=1
worker_publisher: python pub.py --concurrency=1