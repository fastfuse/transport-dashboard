import json
import uuid

from flask import request, jsonify, session, render_template, flash, redirect, \
    url_for
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_user, logout_user, login_required
from flask_socketio import emit, join_room

from app import app, models, db, admin, socketio, redis
from app.forms import LoginForm, RegistrationForm
from app.tasks import monitor_stop
from app.utils import TransportAPIWrapper

# Lviv public transport API wrapper object
transport = TransportAPIWrapper()


# ======================== Admin page

class UserView(ModelView):
    column_exclude_list = ['password_hash', ]


admin.add_view(ModelView(models.Stop, db.session))
admin.add_view(UserView(models.User, db.session))


# ======================== Views


@app.route('/')
@login_required
def test_index():
    users = models.User.query.all()

    return render_template('index2.html', users=users)


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

        flash('Congratulations, you are now a registered user!')

        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('test_index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = models.User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        # login_user(user, remember=form.remember_me.data)
        login_user(user)
        next_page = request.args.get('next', url_for('index'))

        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('test_index'))


# @app.route('/')
@app.route('/dashboard')
def index():
    uid = str(uuid.uuid4())

    session['uid'] = uid

    stops_info = list()

    selected_stops = models.Stop.query.all()

    for stop in selected_stops:
        monitor_stop.apply_async([stop.code, uid], countdown=1)
        stops_info.append(stop)

    return render_template('index.html', data=stops_info)


@app.route('/stops')
def show_all_stops():
    if b'stops' in redis.keys():
        stops = json.loads(redis.get('stops').decode())
    else:
        stops = transport.get_all_stops()
        redis.set('stops', json.dumps(stops))

    user_stops = [stop.code for stop in models.Stop.query.all()]

    return render_template('stops.html', stops=stops, user_stops=user_stops)


@app.route('/routes')
def show_all_routes():
    """
    List all routes.
    """

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
    """
    pass


@app.route('/add_stop', methods=["POST"])
def add_stop():
    stop = models.Stop(internal_id=request.form['internal_id'],
                       name=request.form['name'],
                       code=request.form['code'])

    db.session.add(stop)
    db.session.commit()

    return jsonify(status='OK')


@app.route('/delete_stop', methods=['POST'])
def delete_stop():
    """
    Delete stop from db.
    """
    stop_code = request.form.get('stop_code')

    stop = models.Stop.query.filter_by(code=stop_code).first()

    db.session.delete(stop)
    db.session.commit()

    return jsonify(status='OK')


# ============ socketio ACK

@socketio.on('connect', namespace='/dashboard')
def on_connect():
    print('====================')
    # print(request.sid)
    print('====================')
    # print(session.get('uid'))
    print(session.keys())
    print('==')
    print(session['uid'])

    join_room(session['uid'])
    # s = session.get('uid', 'kek')
    # join room
    # users.append(request.sid)
    # emit('connection_update', {'msg': 'kekekekekek'})
    emit('connection_update', {'msg': 'Server ACK', 'sid': session.get('uid')})
    # emit('connection_update', {'msg': 'Server ACK', 's': s})
    # room=request.sid)


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
# fix socket duplication problem; (dirty hack; make more elegant solution)
# show on map: map w/ marker (modal);
