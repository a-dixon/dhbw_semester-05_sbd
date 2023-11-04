from flask import Blueprint

customer_api_blueprint = Blueprint('customer_api', __name__)

from . import routes
from . import customer_api
