from time import sleep

from app import models, celery
from app.utils import *
from app.tasks import get_stop_info_2

from paho.mqtt.client import Client

t = TransportAPIWrapper()

mqtt_client = Client()
mqtt_client.on_connect = on_connect_pub
mqtt_client.on_publish = on_publish
mqtt_client.on_log = on_log
mqtt_client.on_disconnect = on_disconnect

mqtt_client.connect("broker.hivemq.com")
mqtt_client.loop_start()  # start the loop

# @celery.task
# def get_stop_info_2(stop_code, mq):
#     """
#     Get stop monitoring data. When ready - send data to UI through socket.
#     """
#
#     info = t.monitor_stop(stop_code)
#
#     data = {
#         'stop': stop_code,
#         'info': info[:5],
#     }
#
#     rc, mid = mq.publish(topic=f"transport/stop/{stop_code}",
#                                   payload=json.dumps(data), retain=True)
#
#     # emit to user's personal room (user.room)
#     # socketio.emit('update', data, namespace='/dashboard', room=room)
#
#     return rc, mid


if __name__ == '__main__':

    # t = TransportAPIWrapper()

    # mqtt_client = Client()
    # mqtt_client.on_connect = on_connect_pub
    # mqtt_client.on_publish = on_publish
    # mqtt_client.on_log = on_log
    # mqtt_client.on_disconnect = on_disconnect
    #
    # mqtt_client.connect("broker.hivemq.com")
    # mqtt_client.loop_start()  # start the loop

    stops = models.Stop.query.all()
    stops_codes = [stop.code for stop in stops]

    while True:
        print('Start...')

        stops = models.Stop.query.all()

        stops_codes = [stop.code for stop in stops]

        routes = t.get_all_routes()

        for code in stops_codes:
            get_stop_info_2.apply_async([code], countdown=1)
            # info = t.monitor_stop(code)

            # data = {
            #     'stop': code,
            #     'info': info[:5]
            # }

            # rc, mid = mqtt_client.publish(topic=f"transport/stop/{code}",
            #                               payload=json.dumps(data), retain=True)
            # print(rc, mid)

            # if rc != 0:
            #     print("Error while publishing...")

        # rc, mid = mqtt_client.publish(topic="transport/test",
        #                               payload=json.dumps(routes))

        # print(rc, mid)
        print('sleep...')
        sleep(30)

# TODO:
# * handle errors;
# * add logging;


# * requests timeout + retry investigate

# pseudocode:
# while true:
#     ...
#     for stop in stops:
#         execute(stop)
#
#     sleep(30)

# looks_lively_listener
