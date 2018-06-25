"""
API views.
"""
from flask import jsonify

from application.utils import TransportAPIWrapper
from . import api_blueprint

# Lviv public transport API wrapper object
transport = TransportAPIWrapper()


@api_blueprint.route('/stops')
def stops_api():
    stops = transport.get_all_stops()
    return jsonify(count=len(stops), stops=stops)


@api_blueprint.route('/routes')
def routes_api():
    routes = transport.get_all_routes()
    return jsonify(count=len(routes), routes=routes)
