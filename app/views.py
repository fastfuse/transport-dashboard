from app import app, models
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


@app.route('/test')
def t():
    users = models.User.query.all()
    for u in users:
        print(u.name, u.id)
    return render_template('index.html', users=users)


# ===============

@app.route('/api/stops')
def api_stops():
    stops = transport.get_all_stops()
    return jsonify(stops=stops, count=len(stops))


@app.route('/api/routes')
def api_routes():
    routes = transport.get_all_routes()
    return jsonify(routes=routes, count=len(routes))
