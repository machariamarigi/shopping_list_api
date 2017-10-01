"""Module containing resplus models used in the API"""
from flask_restplus import fields

from api_v1.authenticate import auth

register_args_model = auth.model(
    'registration_args',
    {
        'email': fields.String(required=True, default="user@example.com"),
        'password': fields.String(required=True, default="password_example"),
        'username': fields.String(required=True, default="user_example"),
    }
)

login_args_model = auth.model(
    'login_args_model',
    {
        'email': fields.String(required=True, default="user@example.com"),
        'password': fields.String(required=True, default="password_example")
    }
)