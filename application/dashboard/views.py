"""
Dashboard views.
"""

import json

from flask import request, jsonify, session, render_template
from flask_login import current_user

from application import app, models, db, redis
from application.utils import TransportAPIWrapper

# Lviv public transport API wrapper object
transport = TransportAPIWrapper()


@app.route('/')
@app.route('/dashboard')
def index():
    if not current_user.is_authenticated:
        return render_template('index.html')

    personal_room = session.get('personal_room')
    selected_stops = [{'name': stop.name, 'code': stop.code} for stop in
                      current_user.stops]

    return render_template('index.html', data=selected_stops,
                           room=personal_room)


@app.route('/stops')
def show_all_stops():
    """
    List all stops.
    """
    # TODO: add pagination

    stops = redis.get('stops')

    if not stops:
        stops = transport.get_all_stops()
        redis.set('stops', json.dumps(stops))
    else:
        stops = json.loads(stops.decode())

    if current_user.is_authenticated:
        user_stops = [stop.code for stop in current_user.stops]
    else:
        user_stops = list()

    return render_template('stops.html', stops=stops, user_stops=user_stops)


@app.route('/routes')
def show_all_routes():
    """
    List all routes.
    """
    # TODO: add pagination
    redis.delete('routes')

    routes = redis.get('routes')

    if not routes:
        routes_api = transport.get_all_routes()
        routes = {route['external_id']: route for route in routes_api}
        # cache
        redis.set('routes', json.dumps(routes))
    else:
        routes = json.loads(routes.decode())

    return render_template('routes.html', routes=routes)


@app.route('/route/<route_id>')
def show_route_stops(route_id):
    """
    List all stops on route.
    """
    # TODO: add pagination

    routes = redis.get('routes')

    if not routes:
        routes = transport.get_all_routes()
        # cache
        redis.set('routes', json.dumps(routes))
    else:
        routes = json.loads(routes.decode())

    route = routes.get(route_id)

    if current_user.is_authenticated:
        user_stops = [stop.code for stop in current_user.stops]
    else:
        user_stops = list()

    return render_template('route_stops.html', route=route, user_stops=user_stops)


@app.route('/add_stop', methods=["POST"])
def add_stop():
    stop = models.Stop.query.filter_by(
        external_id=request.form['external_id']).first()

    if not stop:
        stop = models.Stop(external_id=request.form['external_id'],
                           name=request.form['name'],
                           code=request.form['code'],
                           latitude=request.form['lat'],
                           longitude=request.form['lng']
                           )

    current_user.stops.append(stop)

    db.session.add(current_user)
    db.session.commit()

    return jsonify(status='OK')


@app.route('/monitor_stop/<stop_code>')
def monitor_stop(stop_code):
    """
    Get info about certain stop.
    """

    stop_info = transport.monitor_stop(stop_code)

    return render_template('stop_info.html', stop_info=stop_info)


@app.route('/delete_stop', methods=['POST'])
def delete_stop():
    """
    Delete stop from user's stops.
    """
    stop_code = request.form.get('stop_code')
    stop = models.Stop.query.filter_by(code=stop_code).first()

    if len(stop.users) == 1:
        db.session.delete(stop)
    else:
        current_user.stops.remove(stop)
        db.session.add(current_user)

    db.session.commit()

    return jsonify(status='OK')


@app.route('/clean_cache')
def clean_cache():
    """
    Clean Redis cache.
    """
    stops = redis.get('stops')

    if stops:
        redis.delete('stops')

    routes = [k for k in redis.keys() if b'route' in k]

    if routes:
        for r in routes:
            redis.delete(r)

    return jsonify(status='OK')
