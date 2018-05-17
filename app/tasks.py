"""
Celery tasks
"""
from app import celery, socketio
from app.utils import TransportAPIWrapper

# Lviv public transport API wrapper object
transport = TransportAPIWrapper()


@celery.task
def monitor_stop(stop_code):
    # TODO: rename
    # when ready - send data to UI through socket

    info = transport.monitor_stop(stop_code)

    data = {
        'stop': stop_code,
        'info': info[:5]
    }

    socketio.emit('update', data, namespace='/dashboard')

    return True