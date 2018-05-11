from app import app
from flask import render_template, jsonify
from app.utils import TransportAPIWrapper

transport = TransportAPIWrapper()

STOPS = ('0057', '0232')


@app.route('/')
@app.route('/dashboard')
def index():
    stops_info = list()

    for stop in STOPS:
        info = transport.monitor_stop(stop)
        stops_info.append({'code': stop, 'data': info})

    return render_template('index.html', data=stops_info)


@app.route('/api/stops')
def stops_api():
    stops = transport.get_all_stops()
    return jsonify(count=len(stops), stops=stops)


@app.route('/api/routes')
def routes_api():
    routes = transport.get_all_routes()
    return jsonify(count=len(routes), routes=routes)
