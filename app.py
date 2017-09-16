"""Module containing factory function for the application"""
from flask import Flask
from flask_restplus import Api

from config import app_config
from api_v1 import Blueprint_apiV1
from api_v1.models import db


Api_V1 = Api(
    app=Blueprint_apiV1,
    title="Shopping List Api",
    description="An API for a Shopping List Application",
    contact="machariamarigi@gmail.com"
)


def create_app(environment):
    """Factory function for the application"""
    app = Flask(__name__)
    app.config.from_object(app_config[environment])
    db.init_app(app)

    app.register_blueprint(Blueprint_apiV1)
    # add urls here

    return app
