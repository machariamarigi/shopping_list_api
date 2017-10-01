"""Blueprint for our Version 1 API"""
from flask import Blueprint
from flask_restplus import Namespace

Blueprint_apiV1 = Blueprint('api', __name__, url_prefix="/api/v1")

auth = Namespace(
    "Auth", description='Operations related to Authentication', path='/auth')

from . import errors
