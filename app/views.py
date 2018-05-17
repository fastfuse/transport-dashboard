import json

from flask import request, render_template, jsonify, url_for, redirect
from flask_admin.contrib.sqla import ModelView
from flask_socketio import emit

from app import app, models, db, admin, socketio, redis
from app.utils import TransportAPIWrapper
from app.tasks import monitor_stop

# Lviv public transport API wrapper object
transport = TransportAPIWrapper()

# ======================== Admin page

admin.add_view(ModelView(models.Stop, db.session))


# ======================== Views

@app.route('/')
@app.route('/dashboard')
def index():
    stops_info = list()

    selected_stops = models.Stop.query.all()

    for stop in selected_stops:
        monitor_stop.apply_async([stop.code], countdown=2)
        stops_info.append(stop)

    return render_template('index.html', data=stops_info)


@app.route('/stops')
def show_all_stops():
    if b'stops' in redis.keys():
        stops = json.loads(redis.get('stops').decode())
    else:
        stops = transport.get_all_stops()
        redis.set('stops', json.dumps(stops))

    return render_template('stops.html', stops=stops)


@app.route('/routes')
def show_all_routes():
    if b'routes' in redis.keys():
        routes = json.loads(redis.get('routes').decode())
    else:
        routes = transport.get_all_routes()
        redis.set('routes', json.dumps(routes))

    return render_template('routes.html', routes=routes)


@app.route('/add_stop', methods=["POST"])
def add_stop():
    stop = models.Stop(internal_id=request.form['internal_id'],
                       name=request.form['name'],
                       code=request.form['code'])

    db.session.add(stop)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/test', methods=['POST'])
def test():
    # with app.app_context():
    #     socketio.emit('update', {'data': 'test'}, namespace='/dashboard')

    print('teeeeeeest')

    return render_template('index.html')


@socketio.on('connect', namespace='/dashboard')
def on_connect():
    emit('connection_update', {'msg': 'Server ACK'})


@socketio.on('my_event', namespace='/dashboard')
def on_message(message):
    emit('connection_update', {'msg': message['msg']})


# =============== dev purposes

@app.route('/api/stops')
def stops_api():
    stops = transport.get_all_stops()
    return jsonify(count=len(stops), stops=stops)


@app.route('/api/routes')
def routes_api():
    routes = transport.get_all_routes()
    return jsonify(count=len(routes), routes=routes)

# TODO
# fix socket duplication problem;
# cleanup and deploy v.0.1
# show on map: map w/ marker (modal);
