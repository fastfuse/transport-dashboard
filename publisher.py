import logging
from time import sleep

from sqlalchemy.exc import OperationalError

from application import models, tasks

log = logging.getLogger('Publisher')

from paho.mqtt.client import Client

if __name__ == '__main__':

    # # The callback for when the client receives a CONNACK response from the server.
    # def on_connect(client, userdata, flags, rc):
    #     print("Connected with result code " + str(rc))
    #
    #     # Subscribing in on_connect() means that if we lose the connection and
    #     # reconnect then subscriptions will be renewed.
    #     client.subscribe("lwo/transport/stop/*")
    #
    #
    # def on_subscribe(client, userdata, mid, granted_qos):
    #     print(f'subscribed to topic: {mid}')
    #
    #
    # # The callback for when a PUBLISH message is received from the server.
    # def on_message(client, userdata, msg):
    #     print(msg.topic + " " + str(msg.payload))
    #
    #
    # client = Client()
    # client.on_connect = on_connect
    # client.on_message = on_message
    # client.on_subscribe = on_subscribe
    #
    # client.connect("test.mosquitto.org")
    # # client.connect("iot.eclipse.org")
    # # client.connect("broker.hivemq.com")
    #
    # # Blocking call that processes network traffic, dispatches callbacks and
    # # handles reconnecting.
    # # Other loop*() functions are available that give a threaded interface and a
    # # manual interface.
    # client.loop_forever()

    while True:
        try:
            log.info('Start...')

            stops = models.Stop.query.all()

            log.info(f"Found {len(stops)} stops")

            stops_codes = [stop.code for stop in stops]

            for code in stops_codes:
                log.info(f"Getting info for stop code {code}")
                tasks.get_stop_info.delay(code)

            log.info('Sleep...')
            sleep(30)

        except OperationalError as e:
            log.warning('Could not connect to PSQL. Sleep...')
            sleep(5)

# TODO: switch to celery beat
