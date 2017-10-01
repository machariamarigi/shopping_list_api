"""This module contains helper functions used in the API"""
import re


def name_validalidation(name, context):
    """Method used to validate various names"""
    if len(name.strip()) == 0 or not re.match("^[-a-zA-Z0-9_\\s]*$", name):
        message = "Name shouldn't be empty. No special characters"
        response = {
            "message": message + " for " + context + " names",
            context: "null"
        }
        return response, 400
