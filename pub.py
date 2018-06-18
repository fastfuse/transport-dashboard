from time import sleep

from app import models
from app.utils import *

from paho.mqtt.client import Client

if __name__ == '__main__':

    t = TransportAPIWrapper()

    mqtt_client = Client()
    mqtt_client.on_connect = on_connect_pub
    mqtt_client.on_publish = on_publish
    mqtt_client.on_log = on_log
    mqtt_client.on_disconnect = on_disconnect

    mqtt_client.connect("broker.hivemq.com")
    mqtt_client.loop_start()  # start the loop

    rc = 0

    stops = models.Stop.query.all()

    stops_codes = [stop.code for stop in stops]

    while rc == 0:
        print('start...')
        routes = t.get_all_routes()

        for code in stops_codes:
            info = t.monitor_stop(code)

            # rc, mid = mqtt_client.publish(topic=f"transport/stop/{code}",
            rc, mid = mqtt_client.publish(topic=f"transport/test",
                                          payload=json.dumps(info))

            print(rc, mid)

        # rc, mid = mqtt_client.publish(topic="transport/test",
        #                               payload=json.dumps(routes))

        # print(rc, mid)
        print('sleep...')
        sleep(10)
