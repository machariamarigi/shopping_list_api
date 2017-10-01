"""Module that contains request parsers for the API"""
from flask_restplus import reqparse

registration_parser = reqparse.RequestParser()
registration_parser.add_argument(
    'username',
    required=True,
    help='required and must be a string'
)
registration_parser.add_argument(
    'email',
    required=True,
    help='required and must be a string'
)
registration_parser.add_argument(
    'password',
    required=True,
    help='required and must be a string'
)

login_parser = reqparse.RequestParser()
login_parser.add_argument(
    'email',
    required=True,
    help='required and must be a string'
)
login_parser.add_argument(
    'password',
    required=True,
    help='required and must be a string'
)
