"""
Celery tasks.
"""
import json

from app import celery, socketio
from app.utils import TransportAPIWrapper

from paho.mqtt.publish import single

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


@celery.task
def get_stop_info_2(stop_code):
    """
    Get stop monitoring data. When ready - send data to UI through socket.
    """

    info = transport.monitor_stop(stop_code)

    data = {
        'stop': stop_code,
        'info': info[:5],
    }

    rc, mid = single(topic=f"transport/stop/{stop_code}",
                     payload=json.dumps(data), retain=True)

    # emit to user's personal room (user.room)
    # socketio.emit('update', data, namespace='/dashboard', room=room)

    return rc, mid
