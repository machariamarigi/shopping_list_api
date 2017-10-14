"""This module contains registration and login features."""

from flask_restplus import Resource
from sqlalchemy import func

from api_v1 import auth
from api_v1.models import User
from api_v1.serializers import (register_args_model, login_args_model,
                                password_reset_args_model)
from api_v1.helpers import (
    name_validalidation, email_validation, password_generator)
from api_v1.parsers import registration_parser, login_parser, password_reset


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

        validation_name = name_validalidation(username, "users")
        if validation_name:
            return validation_name

        validation_email = email_validation(email)
        if validation_email:
            return validation_email

        if len(password) < 8:
            response = {
                'message': 'Password too short.',
                'status': 'Registration failed'
            }
            return response, 400

        user_email = User.query.filter_by(email=email).first()
        user_username = User.query.filter(
            func.lower(User.username) == username.lower()).first()

        if not user_email and not user_username:
            user = User(email=email, password=password, username=username)
            user.save()
            response = {
                'message': 'Registered successfully, please log in.',
                'status': 'Registered'
            }
            return response, 201
        else:
            messg = 'Email or username already used.' \
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


@auth.route("/reset_password", endpoint='reset_password')
class PasswordReset(Resource):
    """Class to handle resetting of user passwords"""
    @auth.expect(password_reset_args_model)
    def post(self):
        """
            Handle resetting of registered users passwords.
            Resource Url --> /api/v1/auth/reset_password
        """
        args = password_reset.parse_args()
        email = args.get('email')
        new_password = password_generator()

        validation_email = email_validation(email)
        if validation_email:
            return validation_email

        user = User.query.filter_by(email=email).first()
        if user:
            user.password = new_password
            user.save()
            response = {
                "message": "Password has been reset",
                "status": "Reset password succesful!",
                "new_password": new_password
            }
            return response, 200
        else:
            response = {
                'message': 'User email does not exist, Please try again',
                'status': 'Reset password failed!'
            }
            return response, 400
