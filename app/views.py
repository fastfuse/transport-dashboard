
from app import app
from flask import render_template
from app.utils import TransportAPIWrapper

transport = TransportAPIWrapper()

STOPS = ('0057', '0232')


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/test')
def test():

    stops_info = list()

    for stop in STOPS:
        info = transport.monitor_stop(stop)
        stops_info.append({'code': stop, 'data': info})

    return render_template('index.html', data=stops_info)
