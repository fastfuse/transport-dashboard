"""
Celery tasks
"""
from flask import session

from app import celery, socketio
from app.utils import TransportAPIWrapper

# Lviv public transport API wrapper object
transport = TransportAPIWrapper()


@celery.task
def monitor_stop(stop_code, room):
    """
    Get stop monitoring data. When ready - send data to UI through socket.
    """
    # TODO: rename

    info = transport.monitor_stop(stop_code)

    data = {
        'stop': stop_code,
        'info': info[:5],
        'room': room
    }

    # emit to user.uuid (room)
    # room = session.get('uid')
    # socketio.emit('update', data, namespace='/dashboard', room=room)
    socketio.emit('update', data, namespace='/dashboard')

    return True
