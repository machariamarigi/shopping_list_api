"""This module contains registration and login features."""
import re

from flask_restplus import Resource

from api_v1 import auth
from api_v1.models import User
from api_v1.serializers import register_args_model, login_args_model
from api_v1.parsers import registration_parser, login_parser


@auth.route("/register", endpoint='register')
class Registration(Resource):
    """Class to handle registering of new users"""

    @auth.expect(register_args_model)
    def post(self):
        """
            Handle registering of users.
            Resource Url --> /api/v1/auth/register
        """
        args = registration_parser.parse_args()
        username = args['username']
        email = args['email']
        password = args['password']

        if len(name.strip()) == 0 or not re.match("^[a-zA-Z0-9_]*$", username):
            response = {
                'message': 'Username cannot contain special characters.',
                'status': 'Registration failed'
            }
            return response, 400
        if not re.match(r"(^[a-zA-Z0-9_.]+@[a-zA-Z0-9-]+\.[a-z]+$)", email):
            response = {
                'message': 'Incorrect email format.',
                'status': 'Registration failed'
            }
            return response, 400
        if len(password) < 8:
            response = {
                'message': 'Password too short.',
                'status': 'Registration failed'
            }
            return response, 400

        user_email = User.query.filter_by(email=email).first()

        if not user_email:
            user = User(email=email, password=password, username=username)
            user.save()
            response = {
                'message': 'Registered successfully, please log in.',
                'status': 'Registered'
            }
            return response, 201
        else:
            messg = 'Email already used.' \
                    ' Try another one or login if you are already registered'
            response = {
                'message': messg,
                'status': 'Registration failed'
            }
            return response, 400


@auth.route("/login", endpoint='login')
class Login(Resource):
    """Class to login registered users."""

    @auth.expect(login_args_model)
    def post(self):
        """
            Handle logging in of registered users.
            Resource Url --> /api/v1/auth/login
        """

        args = login_parser.parse_args()

        user = User.query.filter_by(email=args['email']).first()
        if user and user.authenticate_password(args['password']):
            access_token = user.generate_token(user.uuid)
            if access_token:
                response = {
                    'message': 'You logged in successfully.',
                    'status': 'Logged in!',
                    'token': access_token.decode()
                }
                return response, 200
        else:
            response = {
                'message': 'Invalid email or password, Please try again',
                'status': 'Login Failed'
            }
            return response, 401
