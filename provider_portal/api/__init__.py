from flask import Blueprint

bp = Blueprint('api', __name__)

from provider_portal.api import api