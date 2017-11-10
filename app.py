"""Module containing factory function for the application"""
from flask import Flask, redirect
from flask_restplus import Api
from flask_cors import CORS

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
    CORS(app)

    app.register_blueprint(Blueprint_apiV1)

    # add namespaces here
    from api_v1 import authenticate
    Api_V1.add_namespace(authenticate.auth)

    from api_v1 import endpoints
    Api_V1.add_namespace(endpoints.sh_ns)

    @app.route('/')
    def reroute():
        """Method to route root path to /api/v1"""
        return redirect('/api/v1')

    return app
