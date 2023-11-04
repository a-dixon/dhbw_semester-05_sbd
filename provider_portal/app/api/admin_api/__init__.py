from flask import Blueprint

admin_api_blueprint = Blueprint('admin_api', __name__)

from . import routes
