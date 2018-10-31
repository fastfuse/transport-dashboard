"""
Utility functions.
"""

from collections import namedtuple

import lxml.html
import requests

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
