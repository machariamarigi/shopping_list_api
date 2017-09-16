"""This module contains registration and login features."""

from flask import make_response, request, jsonify
from flask_restplus import Namespace, Resource, reqparse, fields

from api_v1.models import User

auth = Namespace(
    "Auth", description='Operations related to Authentication', path='/auth')


register_args_model = auth.model(
    'registration_args', {
        'email': fields.String(required=True),
        'password': fields.String(required=True),
        'username': fields.String(required=True),
    })
register_response_model = auth.model('Register_response', {
    'message': fields.String,
    'status': fields.String,
})

parser = reqparse.RequestParser()


@auth.route("/register", endpoint='register')
class Registration(Resource):
    """This class registers a new user."""

    @auth.doc(body=register_args_model)
    @auth.marshal_with(register_response_model, code=201)
    def post(self):
        """Handle registering of users. Url --> /auth/register"""

        parser.add_argument(
            'username',
            required=True,
            help='required and must be a string'
        )
        parser.add_argument(
            'email',
            required=True,
            help='required and must be a string'
        )
        parser.add_argument(
            'password',
            required=True,
            help='required and must be a string'
        )
        args = parser.parse_args()
        user = User.query.filter_by(email=args['email']).first()

        if not user:
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
        else:
            # There is an existing user. We don't want to register users twice
            # Return a message to the user telling them that they they already exist
            response = {
                'message': 'User already exists. Please login.',
                'status': 'Registration failed'
            }

            return response, 202
        # Query to see if the user already exists
        # user = User.query.filter_by(email=request.data['email']).first()

        # if not user:
        #     # There is no user so we'll try to register them
        #     try:
        #         # Register the user
        #         username = self.args['username']
        #         email = post_data['email']
        #         password = post_data['password']
        #         user = User(email=email, password=password, username=username)
        #         user.save()

        #         response = {
        #             'message': 'You registered successfully. Please log in.'
        #         }
        #         # return a response notifying the user that they registered successfully
        #         return make_response(jsonify(response)), 201
        #     except Exception as e:
        #         # An error occured, therefore return a string message containing the error
        #         response = {
        #             'message': str(e)
        #         }
        #         return make_response(jsonify(response)), 401
        # else:
        #     # There is an existing user. We don't want to register users twice
        #     # Return a message to the user telling them that they they already exist
        #     response = {
        #         'message': 'User already exists. Please login.'
        #     }

        #     return make_response(jsonify(response)), 202
