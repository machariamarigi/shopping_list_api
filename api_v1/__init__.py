"""Blueprint for our Version 1 API"""
from flask import Blueprint

Blueprint_apiV1 = Blueprint('api', __name__, url_prefix="/api/v1")

from . import errors
