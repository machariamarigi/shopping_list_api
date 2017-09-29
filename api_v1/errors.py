from flask import jsonify

from . import Blueprint_apiV1 as api_v1


def produce_error(error, code):
    """function to produce error codes and accompaning json messsages"""
    error_dict = {}
    error_dict["error"] = error
    response = jsonify(error_dict)
    response.status_code = code
    return response


@api_v1.app_errorhandler(403)
def forbidden(e):
    return produce_error('forbidden', code=403)


@api_v1.app_errorhandler(404)
def page_not_found(e):
        return produce_error("not found", code=404)


@api_v1.app_errorhandler(500)
def server_errror(e):
    return produce_error('server error', code=500)
