"""This module contains registration and login features."""

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
register_response_model = auth.model(
    'Register_response',
    {
        'message': fields.String,
        'status': fields.String,
    }
)

parser1 = reqparse.RequestParser()
parser2 = reqparse.RequestParser()


@auth.route("/register", endpoint='register')
class Registration(Resource):
    """Class to handle registering of new users"""

    @auth.expect(register_args_model)
    @auth.marshal_with(register_response_model)
    def post(self):
        """Handle registering of users. Url --> /auth/register"""

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
        user_email = User.query.filter_by(email=args['email']).first()

        if not user_email:
            try:
                username = args['username']
                email = args['email']
                password = args['password']
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
            # There is an existing user. We don't want to register users twice
            # Return a message to the user telling them that they they already exist
            response = {
                'message': 'User already exists. Please login.',
                'status': 'Registration failed'
            }
            return response, 202


login_args_model = auth.model(
    'login_args_model',
    {
        'email': fields.String(required=True, default="user@example.com"),
        'password': fields.String(required=True, default="password_example")
    }
)

login_response_model = auth.model(
    'login_repsonse', {
        'message': fields.String,
        'status': fields.String,
        'token': fields.String(default="No Token"),
    })


@auth.route("/login", endpoint='login')
class Login(Resource):
    """Class to login registered users."""

    @auth.expect(login_args_model)
    @auth.marshal_with(login_response_model)
    def post(self):
        """Handle logging in of registered users. Url --> /auth/login"""

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
