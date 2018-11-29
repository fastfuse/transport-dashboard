"""
Celery tasks.
"""
import json
import logging
from time import sleep

from paho.mqtt.publish import single
from sqlalchemy.exc import OperationalError

from application import celery, utils, app, models

log = logging.getLogger('Publisher')

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
        'info': info['timetable'][:5],
    }

    # TODO: add last update (timestamp)

    broker = app.config['MQTT_BROKERS'].get('MOSQUITTO')

    single(hostname=broker,
           topic=f"lwo/transport/stop/{stop_code}",
           payload=json.dumps(data), retain=True)


@celery.task
def publish_stops_info():
    try:
        log.info('Start...')

        stops = models.Stop.query.all()

        log.info(f"Found {len(stops)} stops")

        stops_codes = [stop.code for stop in stops]

        for code in stops_codes:
            log.info(f"Getting info for stop code {code}")
            get_stop_info.delay(code)

        log.info('Sleep...')
        sleep(30)

    except OperationalError as e:
        log.warning('Could not connect to PSQL. Sleep...')
        sleep(5)


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Call update_vehicle_position() every 10 seconds
    sender.add_periodic_task(30.0, publish_stops_info.s(), name='update stops information')
