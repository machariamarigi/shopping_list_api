"""Module containing factory function for the application"""
from flask import Flask

from config import app_config
from api_v1.models import db


def create_app(environment):
    """Factory function for the application"""
    app = Flask(__name__)
    app.config.from_object(app_config[environment])
    db.init_app(app)

    # add urls here

    return app
