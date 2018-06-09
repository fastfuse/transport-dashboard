"""
Utility functions.
"""

import json
from time import sleep

import requests

from paho.mqtt.client import Client

import paho.mqtt.publish as publish

from app import app

BASE_URL = 'http://82.207.107.126:13541/SimpleRide/LAD/SM.WebApi/api'
ALL_ROUTES = BASE_URL + '/CompositeRoute'
ROUTE_PATH = BASE_URL + '/path/?code=LAD|'
ROUTE_MONITORING = BASE_URL + '/RouteMonitoring/?code=LAD|'
ALL_STOPS = BASE_URL + '/stops'
ROUTE_STOPS = BASE_URL + '/CompositeRoute/?code=LAD|'
STOP_INFO = ALL_STOPS + '/?code='


# pay attention:
# route: ?code=<id>
# stop: ?code=<code>


class TransportAPIWrapper:
    """
    Wrapper for Lviv public transport API.
    """

    def get_all_routes(self):
        """
        Method to fetch all available routes.
        :return: routes
        """
        routes = dict()

        resp = requests.get(ALL_ROUTES)

        for route in json.loads(resp.json()):
            id_ = route.get('Id')
            name = route.get('Name')
            code = route.get('Code')

            routes.update(
                {id_: {'internal_id': id_, 'name': name, 'code': code}})

        return routes

    @staticmethod
    def _format_stops(stops_data):
        """
        Helper method to build stops dict.

        :param stops_data: response json

        :return: stops dict
        """
        stops = dict()

        for stop in stops_data:
            id_ = stop.get('Id')
            name = stop.get('Name')
            code = stop.get('Code')
            location = (stop.get('Y'), stop.get('X'))

            stops.update({code: {'internal_id': id_, 'name': name,
                                 'code': code, 'location': location}})
        return stops

    def get_all_stops(self):
        """
        Method to get all available stops.
        """
        resp = requests.get(ALL_STOPS)
        stops = self._format_stops(json.loads(resp.json()))

        return stops

    def get_route_stops(self, route_id):
        """
        Method to get all stops on route.
        """
        resp = requests.get(f"{ROUTE_STOPS}{route_id}")
        stops = self._format_stops(json.loads(resp.json()))

        return stops

    def monitor_route(self, route_id):
        """
        Method to get information about all vehicles on route.
        """
        route_info = dict()
        resp = requests.get(f"{ROUTE_MONITORING}{route_id}")

        # TODO: format

        return json.loads(resp.json())

    def monitor_stop(self, stop_code: str):
        """
        Get information about all vehicles that arrive on certain stop.
        """
        stop_data = list()
        resp = requests.get(f"{STOP_INFO}{stop_code}")

        for item in json.loads(resp.json()):
            vehicle_info = {
                'from': item.get('StartPoint'),
                'to': item.get('EndPoint'),
                'route_id': item.get('RouteId'),
                'route_name': item.get('RouteName'),
                'vehicle_id': item.get('VehicleId'),
                'vehicle_name': item.get('VehicleName'),
                'time_to_point': item.get('TimeToPoint'),
                'location': (item.get('Y'), item.get('X'))
            }

            stop_data.append(vehicle_info)

        return stop_data


# ===================== Custom Jinja template filters

@app.template_filter()
def to_minutes(seconds):
    """
    Convert seconds to minutes.
    """
    return round(seconds / 60)


# ====================== MQTT stuff
# Callbacks required to publish/subscribe messages.

# The callback for when the client receives a CONNACK response from the server.
def on_connect_sub(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("transport/test")


def on_connect_pub(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    print(f"flags: {flags}")


def on_subscribe(client, userdata, mid, granted_qos):
    print(f'Successfully subscribed')


def on_publish(client, userdata, mid):
    print(f"Message Published. mid: {mid}")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(f'Received message from topic: {msg.topic}')
    print(str(msg.payload))


def on_disconnect(client, userdata, rc):
    if rc == 0:
        print("Successfully disconnected.")
    else:
        print("Some error occurred...")


def on_log(client, userdata, level, buf):
    print(f"=== Log: {buf}")


# ======================

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

    while rc == 0:
        print('start...')
        routes = t.get_all_routes()

        rc, mid = mqtt_client.publish(topic="transport/test",
                                      payload=json.dumps(routes))

        print(rc, mid)
        print('sleep...')
        sleep(5)


# ==== client
    # client = Client()
    # client.on_connect = on_connect_sub
    # client.on_message = on_message
    # client.on_subscribe = on_subscribe
    # client.on_log = on_log
    #
    # client.connect("broker.hivemq.com")
    #
    # # Blocking call that processes network traffic, dispatches callbacks and
    # # handles reconnecting.
    # # Other loop*() functions are available that give a threaded interface and a
    # # manual interface.
    # client.loop_forever()
