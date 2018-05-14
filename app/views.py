import json

from flask_admin.contrib.sqla import ModelView

from app import app, models, db, admin, celery
from flask import request, render_template, jsonify, session, url_for, redirect
from app.utils import TransportAPIWrapper

transport = TransportAPIWrapper()

# ======================== Admin page

admin.add_view(ModelView(models.Stop, db.session))


# ======================= celery tasks


@celery.task(bind=True)
def monitor_stop(self, stop_code):
    info = transport.monitor_stop(stop_code)

    # when ready - send data to UI by socket

    return info


# ======================== Views

@app.route('/')
@app.route('/dashboard')
def index():
    stops_info = list()

    tasks = list()

    selected_stops = models.Stop.query.all()

    for stop in selected_stops:
        monitor_stop.delay(stop.code)
        # info = monitor_stop(stop.code)
        # stops_info.append({'stop': stop, 'data': info})
        stops_info.append(stop)

        # tasks.append(monitor_stop(stop.code))

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


@app.route('/test')
def t():
    stop_code = '0247'

    return render_template('index.html', users=users)


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
#
