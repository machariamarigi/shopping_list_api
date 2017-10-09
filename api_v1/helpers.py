"""This module contains helper functions used in the API"""
import datetime
import json
import re
from functools import wraps

from flask import request

from api_v1.models import User


def name_validalidation(name, context):
    """Method used to validate various names"""
    if len(name.strip()) == 0 or not re.match("^[-a-zA-Z0-9_\\s]*$", name):
        message = "Name shouldn't be empty. No special characters"
        response = {
            "message": message + " for " + context + " names",
            context: "null"
        }
        return response, 400


def datetimeconverter(obj):
    """Function to convert datime objects to a string"""
    if isinstance(obj, datetime.datetime):
        return obj.__str__()


def master_serializer(resource):
    """Function to return a resource json"""
    data = resource.serialize()
    user_json = json.dumps(
        data, default=datetimeconverter, sort_keys=True
    )
    return user_json


def token_required(funct):
    """Decorator method to check for jwt tokens"""
    @wraps(funct)
    def wrapper(*args, **kwargs):
        """Wrapper function to add pass down results of the token decoding"""
        if 'Authorization' in request.headers:
            access_token = request.headers.get('Authorization')

            data = User.decode_token(access_token)
            if not isinstance(data, str):
                user_id = data
            else:
                response = {
                    'message': data
                }
                return response, 401

            return funct(*args, user_id, **kwargs)
        else:
            message = "No token found! Ensure that the request header"
            response = {
                'message': message + ' has an authorization key value'
            }
            return response, 401
    wrapper.__doc__ = funct.__doc__
    wrapper.__name__ = funct.__name__
    return wrapper
