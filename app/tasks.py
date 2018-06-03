"""
Celery tasks
"""

from app import celery, socketio
from app.utils import TransportAPIWrapper

# Lviv public transport API wrapper object
transport = TransportAPIWrapper()


@celery.task
def get_stop_info(stop_code, room):
    """
    Get stop monitoring data. When ready - send data to UI through socket.
    """

    info = transport.monitor_stop(stop_code)

    data = {
        'stop': stop_code,
        'info': info[:5],
        'room': room
    }

    # emit to user's personal room (user.room)
    socketio.emit('update', data, namespace='/dashboard', room=room)

    return True
