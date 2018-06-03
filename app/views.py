import json

from flask import request, jsonify, session, render_template, flash, redirect, \
    url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_user, logout_user
from flask_socketio import emit, join_room

from app import app, models, db, admin, socketio, redis
from app.forms import LoginForm, RegistrationForm
from app.tasks import get_stop_info
from app.utils import TransportAPIWrapper

# Lviv public transport API wrapper object
transport = TransportAPIWrapper()


# ================================= Admin page

class SecureModelView(ModelView):
    column_exclude_list = ['password_hash', ]

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin


admin.add_view(SecureModelView(models.Stop, db.session))
admin.add_view(SecureModelView(models.User, db.session))


# ================================= Login stuff


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = models.User(username=form.username.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash('Successfully registered')

        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = models.User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # login_user(user, remember=form.remember_me.data)
        login_user(user)

        # store user's personal room to session
        session['personal_room'] = user.room

        next_page = request.args.get('next', url_for('index'))

        return redirect(next_page)

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# ========================================================

@app.route('/')
@app.route('/dashboard')
def index():
    if not current_user.is_authenticated:
        return render_template('index.html')

    personal_room = session.get('personal_room')
    stops_info = list()
    selected_stops = current_user.stops

    for stop in selected_stops:
        get_stop_info.apply_async([stop.code, personal_room], countdown=1)
        stops_info.append(stop)

    return render_template('index.html', data=stops_info)


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

    routes = redis.get('routes')

    if not routes:
        routes = transport.get_all_routes()
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

    cache_key = f'route_{route_id}'

    routes = redis.get('routes')

    if not routes:
        routes = transport.get_all_routes()
        # cache
        redis.set('routes', json.dumps(routes))
    else:
        routes = json.loads(routes.decode())

    route = routes.get(route_id)

    if cache_key.encode() in redis.keys():
        route_stops = json.loads(redis.get(cache_key).decode())
    else:
        route_stops = transport.get_route_stops(route_id)
        # store to cache
        redis.set(cache_key, json.dumps(route_stops))

    user_stops = [stop.code for stop in models.Stop.query.all()]

    return render_template('route_stops.html', route=route, stops=route_stops,
                           user_stops=user_stops)


@app.route('/route_map/<route_id>')
def show_route_map(route_id):
    """
    Display route on map.
    TDB.
    """
    pass


@app.route('/add_stop', methods=["POST"])
def add_stop():
    stop = models.Stop.query.filter_by(
        internal_id=request.form['internal_id']).first()

    if not stop:
        stop = models.Stop(internal_id=request.form['internal_id'],
                           name=request.form['name'],
                           code=request.form['code'],
                           latitude=request.form['lat'],
                           longitude=request.form['lng']
                           )

    current_user.stops.append(stop)

    db.session.add(current_user)
    db.session.commit()

    # TODO: display success on UI somehow
    return jsonify(status='OK')


@app.route('/monitor_stop/<stop_code>')
def monitor_stop(stop_code):
    """
    Get info about certain stop.
    """
    stops = redis.get('stops')

    if not stops:
        stops = transport.get_all_stops()
        redis.set('stops', json.dumps(stops))
    else:
        stops = json.loads(stops.decode())

    stop = stops.get(stop_code)
    stop_info = transport.monitor_stop(stop_code)

    return render_template('stop_info.html', stop=stop, stop_info=stop_info)


@app.route('/delete_stop', methods=['POST'])
def delete_stop():
    """
    Delete stop from user's stops.
    """
    stop_code = request.form.get('stop_code')
    stop = models.Stop.query.filter_by(code=stop_code).first()
    current_user.stops.remove(stop)

    db.session.add(current_user)
    db.session.commit()

    return jsonify(status='OK')


# ============ socketio ACK

@socketio.on('connect', namespace='/dashboard')
def on_connect():
    room = session.get('personal_room')

    # join personal room
    join_room(room)
    emit('connection_update', {'msg': 'Server ACK', 'sid': room})


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

# =======================

# TODO
# show on map: map w/ marker (modal);
