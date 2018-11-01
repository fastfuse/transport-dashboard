"""
Dashboard views.
"""

import json

from flask import request, jsonify, session, render_template
from flask_login import current_user

from application import app, models, db, redis
from application.utils import TransportAPIWrapper

# Lviv public transport API wrapper object
# transport = TransportAPIWrapper()


@app.route('/')
@app.route('/dashboard')
def index():
    return "Hello World!"
