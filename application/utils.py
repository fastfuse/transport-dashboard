"""
Utility functions.
"""

import json
import math
from collections import namedtuple

import lxml.html
import requests

# from application import app

# BASE_URL = 'http://82.207.107.126:13541/SimpleRide/LAD/SM.WebApi/api'
# ALL_ROUTES = BASE_URL + '/CompositeRoute'
# ROUTE_PATH = BASE_URL + '/path/?code=LAD|'
# ROUTE_MONITORING = BASE_URL + '/RouteMonitoring/?code=LAD|'
# ALL_STOPS = BASE_URL + '/stops'
# ROUTE_STOPS = BASE_URL + '/CompositeRoute/?code=LAD|'
# STOP_INFO = ALL_STOPS + '/?code='


# pay attention:
# route: ?code=<id>
# stop: ?code=<code>


# class TransportAPIWrapper:
#     """
#     Wrapper for Lviv public transport API.
#     """
#
#     def get_all_routes(self):
#         """
#         Method to fetch all available routes.
#         :return: routes
#         """
#         routes = dict()
#
#         resp = requests.get(ALL_ROUTES)
#
#         for route in json.loads(resp.json()):
#             id_ = route.get('Id')
#             name = route.get('Name')
#             code = route.get('Code')
#
#             routes.update(
#                 {id_: {'internal_id': id_, 'name': name, 'code': code}})
#
#         return routes
#
#     @staticmethod
#     def _format_stops(stops_data):
#         """
#         Helper method to build stops dict.
#
#         :param stops_data: response json
#
#         :return: stops dict
#         """
#         stops = dict()
#
#         for stop in stops_data:
#             id_ = stop.get('Id')
#             name = stop.get('Name')
#             code = stop.get('Code')
#             location = (stop.get('Y'), stop.get('X'))
#
#             stops.update({code: {'internal_id': id_, 'name': name,
#                                  'code': code, 'location': location}})
#         return stops
#
#     def get_all_stops(self):
#         """
#         Method to get all available stops.
#         """
#         resp = requests.get(ALL_STOPS)
#         stops = self._format_stops(json.loads(resp.json()))
#
#         return stops
#
#     def get_route_stops(self, route_id):
#         """
#         Method to get all stops on route.
#         """
#         resp = requests.get(f"{ROUTE_STOPS}{route_id}")
#         stops = self._format_stops(json.loads(resp.json()))
#
#         return stops
#
#     def monitor_route(self, route_id):
#         """
#         Method to get information about all vehicles on route.
#         """
#         route_info = dict()
#         resp = requests.get(f"{ROUTE_MONITORING}{route_id}")
#
#         # TODO: format
#
#         return json.loads(resp.json())
#
#     def monitor_stop(self, stop_code: str):
#         """
#         Get information about all vehicles that arrive on certain stop.
#         """
#         stop_data = list()
#         resp = requests.get(f"{STOP_INFO}{stop_code}")
#
#         for item in json.loads(resp.json()):
#             vehicle_info = {
#                 'from': item.get('StartPoint'),
#                 'to': item.get('EndPoint'),
#                 'route_id': item.get('RouteId'),
#                 'route_name': item.get('RouteName'),
#                 'vehicle_id': item.get('VehicleId'),
#                 'vehicle_name': item.get('VehicleName'),
#                 'time_to_point': item.get('TimeToPoint'),
#                 'location': (item.get('Y'), item.get('X'))
#             }
#
#             stop_data.append(vehicle_info)
#
#         return stop_data


BASE_URL = 'https://lad.lviv.ua'
ALL_ROUTES = BASE_URL + '/api/routes'
ROUTE_PATH = BASE_URL + '/path/?code=LAD|'
ROUTE_MONITORING = BASE_URL + '/RouteMonitoring/?code=LAD|'
ALL_STOPS = BASE_URL + '/stops'
ROUTE_STOPS = BASE_URL + '/CompositeRoute/?code=LAD|'
STOP_INFO = BASE_URL + '/api/stops/{code}'

stop_object = namedtuple("Stop", ['name', 'longitude', 'latitude', 'external_id', 'code'])


class TransportAPIWrapper:
    """
    Wrapper for Lviv public transport API.
    """

    def get_all_routes(self):
        """
        Method to fetch all available routes.
        :return: routes
        """

        routes = requests.get(ALL_ROUTES).json()

        stops = self.get_all_stops()

        for route in routes:
            stops_list = [stops.get(str(stop_code)) for stop_code in route['stops']]
            route['stops'] = stops_list

        return routes

    def get_all_stops(self):
        """
        Method to get all available stops.
        """
        data = requests.get(ALL_STOPS)

        parsed_stops_root = lxml.html.fromstring(data.text)

        stops_data = [[child.text for child in ps.getchildren()] for ps in parsed_stops_root.xpath('//tr')[1:]]

        stops_objects = [stop_object(*s[:-1]) for s in stops_data]

        stops = {stop.code: stop._asdict() for stop in stops_objects}

        return stops

    def monitor_stop(self, stop_code: str):
        """
        Get information about all vehicles that arrive on certain stop.
        """
        resp = requests.get(STOP_INFO.format(code=stop_code)).json()

        return resp

# ============= Custom Jinja template filters.

# @app.template_filter()
# def to_minutes(seconds):
#     """
#     Convert seconds to minutes.
#     """
#     return math.floor(seconds / 60)
#
#
# if __name__ == '__main__':
#     t = TransportAPIWrapper()
