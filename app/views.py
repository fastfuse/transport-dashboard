import json

from flask import request, render_template, jsonify, session, url_for, redirect
from flask_admin.contrib.sqla import ModelView
from flask_socketio import emit

from app import app, models, db, admin, celery, socketio
from app.utils import TransportAPIWrapper

# api wrapper object
transport = TransportAPIWrapper()

# ======================== Admin page

admin.add_view(ModelView(models.Stop, db.session))


# ======================= celery tasks

@celery.task
def monitor_stop(stop_code):
    # TODO: rename
    # when ready - send data to UI through socket

    info = transport.monitor_stop(stop_code)

    data = {
        'stop': stop_code,
        'info': info
    }

    socketio.emit('update', data, namespace='/dashboard')

    return True


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
    if 'stops' in session.keys():
        stops = json.loads(session.get('stops'))
    else:
        stops = transport.get_all_stops()
        session['stops'] = json.dumps(stops)

    return render_template('stops.html', stops=stops)


@app.route('/routes')
def show_all_routes():
    if 'routes' in session.keys():
        routes = json.loads(session.get('routes'))
    else:
        routes = transport.get_all_routes()
        session['routes'] = json.dumps(routes)

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
    emit('update', {'data': 'Connected', 'count': 0})


@socketio.on('my_event', namespace='/dashboard')
def on_message(message):
    emit('update', {'data': message['data'], 'count': 2})


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
# * celery + sockets;
# * show on map: map w/ marker (modal);
