"""This module contains registration and login features."""
import re

from flask_restplus import Namespace, Resource, reqparse, fields

from api_v1.models import User

auth = Namespace(
    "Auth", description='Operations related to Authentication', path='/auth')


register_args_model = auth.model(
    'registration_args',
    {
        'email': fields.String(required=True, default="user@example.com"),
        'password': fields.String(required=True, default="password_example"),
        'username': fields.String(required=True, default="user_example"),
    }
)

parser1 = reqparse.RequestParser()
parser2 = reqparse.RequestParser()


@auth.route("/register", endpoint='register')
class Registration(Resource):
    """Class to handle registering of new users"""

    @auth.expect(register_args_model)
    def post(self):
        """
            Handle registering of users.
            Resource Url --> /api/v1/auth/register
        """

        parser1.add_argument(
            'username',
            required=True,
            help='required and must be a string'
        )
        parser1.add_argument(
            'email',
            required=True,
            help='required and must be a string'
        )
        parser1.add_argument(
            'password',
            required=True,
            help='required and must be a string'
        )
        args = parser1.parse_args()
        username = args['username']
        email = args['email']
        password = args['password']

        if not re.match("^[a-zA-Z0-9_]*$", username):
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
            try:
                user = User(email=email, password=password, username=username)
                user.save()
                response = {
                    'message': 'Registered successfully, please log in.',
                    'status': 'Registered'
                }
                return response, 201
            except Exception as e:
                response = {
                    'message': str(e)
                }
                return response, 500
        else:
            messg = 'Email already used.' \
                    ' Try another one or login if you are already registered'
            response = {
                'message': messg,
                'status': 'Registration failed'
            }
            return response, 400


login_args_model = auth.model(
    'login_args_model',
    {
        'email': fields.String(required=True, default="user@example.com"),
        'password': fields.String(required=True, default="password_example")
    }
)


@auth.route("/login", endpoint='login')
class Login(Resource):
    """Class to login registered users."""

    @auth.expect(login_args_model)
    def post(self):
        """
            Handle logging in of registered users.
            Resource Url --> /api/v1/auth/login
        """

        parser2.add_argument(
            'email',
            required=True,
            help='required and must be a string'
        )
        parser2.add_argument(
            'password',
            required=True,
            help='required and must be a string'
        )

        args2 = parser2.parse_args()

        try:
            user = User.query.filter_by(email=args2['email']).first()
            if user and user.authenticate_password(args2['password']):
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

        except Exception as e:
            response = {
                'message': str(e)
            },
            return response, 500
