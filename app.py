from flask import Flask

from config import app_config
from models import db
from api_endpoints import api


def create_app(environment):
    """Factory function for the application"""
    app = Flask(__name__)
    app.config.from_object(app_config[environment])

    return app
