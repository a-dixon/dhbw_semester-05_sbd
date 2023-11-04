from flask import Blueprint

smartmeter_api_blueprint = Blueprint('smartmeter_api', __name__)

from . import routes
