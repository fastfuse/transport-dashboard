"""
Celery tasks.
"""
import json

from paho.mqtt.publish import single

from application import celery, utils

# Lviv public transport API wrapper object
transport = utils.TransportAPIWrapper()


@celery.task
def get_stop_info(stop_code):
    """
    Get stop monitoring data.
    """

    info = transport.monitor_stop(stop_code)

    data = {
        'stop': stop_code,
        'info': info[:5],
    }

    # TODO: add last update (timestamp)

    single(hostname="broker.hivemq.com",
           topic=f"lwo/transport/stop/{stop_code}",
           payload=json.dumps(data), retain=True)
