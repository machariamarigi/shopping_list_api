"""
    Main module for the api containing the factory function for the
    application
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import app_config

db = SQLAlchemy()


def create_app(config_name):
    """
        Factory function that creates instance of the app with a given
        configuration
        Args:
            config_name(str): Name of the configuration to create app
        Returns:
            app(obj->Flask): Return instance of the app
    """

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')


    from .api_v1 import api as api_v1_blueprint
    app.register_blueprint(api_v1_blueprint, url_prefix="/api/v1")

    return app
