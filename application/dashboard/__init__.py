from flask import Blueprint

dashboard_blueprint = Blueprint('dashboard_blueprint', __name__)

from . import views
