"""This module contains the API endpoints in regards to the shopping lists"""
import datetime
import json
import re
from functools import wraps

from flask import request
from flask_restplus import Namespace, fields, Resource, reqparse
from sqlalchemy import func

from api_v1.models import Shoppinglist, Shoppingitem, User


def datetimeconverter(obj):
    """Function to convert datime objects to a string"""
    if isinstance(obj, datetime.datetime):
        return obj.__str__()


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
    wrapper.__doc__ = funct.__doc__
    wrapper.__name__ = funct.__name__
    return wrapper

sh_ns = Namespace(
    "Shoppinglist Endpoints",
    description="Operations related to Shoppinglists and Items",
    path="/"
)

shoppinglist_model = sh_ns.model('ShoppingList', {
    'name': fields.String(required=True, default="Groceries")
})


@sh_ns.header(
    "Authorization",
    description="JWT token for authenticationg users",
    required=True
)
@sh_ns.route("/shoppinglists")
class Shoppinglists(Resource):
    """Class to handle multiple shoppinglists"""

    @sh_ns.expect(shoppinglist_model)
    @token_required
    def post(self, user_id):
        """
            Handle posting of new shoppinglists for an authorized user.
            Resource Url --> /api/v1/shoppinglists
        """
        parser = reqparse.RequestParser()

        parser.add_argument(
            'name',
            required=True,
            help="Required and must be a string"
        )

        args = parser.parse_args()
        name = args['name']

        if not re.match("^[-a-zA-Z0-9_\\s]*$", name):
            response = {
                "message": "No special characters for shopping list names",
                "shoppinglist": "null"
            }
            return response, 400

        existing_shoppinglist = Shoppinglist.query.filter(
            func.lower(Shoppinglist.name) == name.lower(),
            Shoppinglist.created_by == user_id
        ).first()

        if existing_shoppinglist:
            response = {
                "message": "Shopping list already exists!",
                "shoppinglist": "null"
            }
            return response, 400

        shoppinglist = Shoppinglist(name=name, created_by=user_id)
        shoppinglist.save()
        data = shoppinglist.serialize()
        sh_json = json.dumps(
            data, default=datetimeconverter, sort_keys=True
        )
        response = {
            "message": "Shopping List created",
            "shoppinglist": json.loads(sh_json)
        }
        return response, 201

    @token_required
    def get(self, user_id):
        """
            Handle getting of all shoppinglists for an authorized user.
            Resource Url --> /api/v1/shoppinglists
        """
        shoppinglists = Shoppinglist.query.filter_by(created_by=user_id)
        results = []

        for shoppinglist in shoppinglists:
            data = shoppinglist.serialize()
            sh_json = json.dumps(
                data, default=datetimeconverter, sort_keys=True
            )
            results.append(json.loads(sh_json))

        response = {
            "message": "Users shoppinglists found!",
            "shoppinglists": results
        }
        return response, 200


@sh_ns.header(
    "Authorization",
    description="JWT token for authenticationg users",
    required=True
)
@sh_ns.route('/shoppinglist/<int:list_id>')
class SingleShoppinglist(Resource):
    """Class to handle operations on a single shopping list"""

    @token_required
    def get(self, user_id, list_id):
        """
            Handle getting of a shoppinglist for an authorized user via an id
            Resource Url --> /api/v1/shoppinglist/<list_id>
        """
        shoppinglist = Shoppinglist.query.filter_by(
            uuid=list_id, created_by=user_id).first()

        if not shoppinglist:
            response = {
                "message": "Shopping list not found"
            }
            return response, 404

        data = shoppinglist.serialize()
        sh_json = json.dumps(
            data, default=datetimeconverter, sort_keys=True
        )
        response = {
            "message": "Shopping list found!",
            "shoppinglist": json.loads(sh_json)
        }
        return response, 200

    @token_required
    def put(self, user_id, list_id):
        """
            Handle updating of a shoppinglist for an authorized user via an id
            Resource Url --> /api/v1/shoppinglist/<list_id>
        """

        parser = reqparse.RequestParser()

        parser.add_argument(
            'name',
            required=True,
            help="Required and must be a string"
        )

        args = parser.parse_args()
        name = args['name']

        shoppinglist = Shoppinglist.query.filter_by(
            uuid=list_id, created_by=user_id).first()

        if not shoppinglist:
            response = {
                "message": "Shopping list not found"
            }
            return response, 404

        if not re.match("^[-a-zA-Z0-9_\\s]*$", name):
            response = {
                "message": "No special characters for shopping list names",
                "shoppinglist": "null"
            }
            return response, 400

        existing_shoppinglist = Shoppinglist.query.filter(
            func.lower(Shoppinglist.name) == name.lower(),
            Shoppinglist.created_by == user_id
        ).first()
        if existing_shoppinglist:
            if name != shoppinglist.name:
                response = {
                    "message": "Shopping list already exists!",
                    "shoppinglist": "null"
                }
                return response, 400

        shoppinglist.name = name
        shoppinglist.save()
        data = shoppinglist.serialize()
        sh_json = json.dumps(
            data, default=datetimeconverter, sort_keys=True
        )
        response = {
            "message": "Shopping List updated!",
            "shoppinglist": json.loads(sh_json)
        }
        return response, 200

    @token_required
    def delete(self, user_id, list_id):
        """
            Handle deleting of a shoppinglist for an authorized user via an id
            Resource Url --> /api/v1/shoppinglist/<list_id>
        """
        shoppinglist = Shoppinglist.query.filter_by(
            uuid=list_id, created_by=user_id).first()

        if not shoppinglist:
            response = {
                "message": "Shopping list not found"
            }
            return response, 404

        shoppinglist.delete()
        message = "Shopping list {} deleted!".format(shoppinglist.name)
        response = {
            "message": message
        }
        return response, 200


item_model = sh_ns.model(
    'Item', {
        'name': fields.String(required=True, default="Carrots"),
        'quantity': fields.Integer(required=True, default=1)
    }
)


@sh_ns.header(
    "Authorization",
    description="JWT token for authenticationg users",
    required=True
)
@sh_ns.route("/shoppinglist/<int:list_id>/items")
class Items(Resource):
    """Class to handle operations of shopping items"""

    @sh_ns.expect(item_model)
    @token_required
    def post(self, user_id, list_id):
        """
            Handle posting of new items to a shopping list
            Resource Url --> /api/v1/shoppinglist/<int:list_id>/items
        """
        del user_id
        parser = reqparse.RequestParser()

        parser.add_argument(
            'name',
            required=True,
            type=str,
            help="Required and must be a string"
        )

        parser.add_argument(
            'quantity',
            required=True,
            type=int,
            help="Required and must be an integer"
        )

        args = parser.parse_args()
        name = args['name']
        quantity = args['quantity']

        if not re.match("^[-a-zA-Z0-9_\\s]*$", name):
            response = {
                "message": "No special characters for item names",
                "item": "null"
            }
            return response, 400

        existing_item = Shoppingitem.query.filter(
            func.lower(Shoppingitem.name) == name.lower(),
            Shoppingitem.shoppinglist == list_id
        ).first()

        if existing_item:
            response = {
                "message": "Item already exists in this shopping list!",
                "item": "null"
            }
            return response, 400

        item = Shoppingitem(
            name=name, quantity=quantity, shoppinglist=list_id)
        item.save()
        data = item.serialize()
        item_json = json.dumps(
            data, default=datetimeconverter, sort_keys=True
        )
        response = {
            "message": "Shopping List created",
            "item": json.loads(item_json)
        }
        return response, 201

    @token_required
    def get(self, user_id, list_id):
        """
            Handle getting of all items for a shoppinglist.
            Resource Url --> /api/v1/shoppinglist/<int:list_id>/items
        """
        del user_id
        items = Shoppingitem.query.filter_by(shoppinglist=list_id)
        results = []

        for item in items:
            data = item.serialize()
            item_json = json.dumps(
                data, default=datetimeconverter, sort_keys=True
            )
            results.append(json.loads(item_json))

        response = {
            "message": "Shopping list's items found",
            "items": results
        }
        return response, 200


@sh_ns.header(
    "Authorization",
    description="JWT token for authenticationg users",
    required=True
)
@sh_ns.route('/shoppinglist/<int:list_id>/item/<int:item_id>')
class SingleItem(Resource):
    """Class to handle operations on a single items in a shopping list"""

    @token_required
    def get(self, user_id, list_id, item_id):
        """
            Handle getting of an item in a shopping list via an id
            Resource Url --> /api/v1/shoppinglist/<list_id>/item/<item_id>
        """

        shoppinglist = Shoppinglist.query.filter_by(
            uuid=list_id, created_by=user_id).first()

        if not shoppinglist:
            response = {
                "message": "Shopping list not found. Item does not exist"
            }
            return response, 404

        item = Shoppingitem.query.filter_by(
            uuid=item_id, shoppinglist=list_id).first()

        if not item:
            response = {
                "message": "Item does not exist found in shopping list"
            }
            return response, 404

        data = item.serialize()
        item_json = json.dumps(
            data, default=datetimeconverter, sort_keys=True
        )
        response = {
            "message": "Shopping list found!",
            "item": json.loads(item_json)
        }
        return response, 200

    @token_required
    def put(self, user_id, list_id, item_id):
        """
            Handle editing of an item in a shopping list via an id
            Resource Url --> /api/v1/shoppinglist/<list_id>/item/<item_id>
        """

        parser = reqparse.RequestParser()

        parser.add_argument(
            'name',
            required=True,
            type=str,
            help="Required and must be a string"
        )

        parser.add_argument(
            'quantity',
            required=True,
            type=int,
            help="Required and must be an integer"
        )

        args = parser.parse_args()
        name = args['name']
        quantity = args['quantity']

        shoppinglist = Shoppinglist.query.filter_by(
            uuid=list_id, created_by=user_id).first()

        if not shoppinglist:
            response = {
                "message": "Shopping list not found. Item does not exist"
            }
            return response, 404

        item = Shoppingitem.query.filter_by(
            uuid=item_id, shoppinglist=list_id).first()

        if not item:
            response = {
                "message": "Item does not exist found in shopping list"
            }
            return response, 404

        if not re.match("^[-a-zA-Z0-9_\\s]*$", name):
            response = {
                "message": "No special characters for item names",
                "item": "null"
            }
            return response, 400

        existing_item = Shoppingitem.query.filter(
            func.lower(Shoppingitem.name) == name.lower(),
            Shoppingitem.shoppinglist == list_id
        ).first()
        if existing_item:
            if name != item.name:
                response = {
                    "message": "Item already exists!",
                    "item": "null"
                }
                return response, 400

        item.name = name
        item.quantity = quantity
        item.save()
        data = item.serialize()
        item_json = json.dumps(
            data, default=datetimeconverter, sort_keys=True
        )
        response = {
            "message": "Item updated!",
            "item": json.loads(item_json)
        }
        return response, 200

    @token_required
    def patch(self, user_id, list_id, item_id):
        """
            Handle buying of an item in a shopping list via an id
            Resource Url --> /api/v1/shoppinglist/<list_id>/item/<item_id>
        """
        shoppinglist = Shoppinglist.query.filter_by(
            uuid=list_id, created_by=user_id).first()

        if not shoppinglist:
            response = {
                "message": "Shopping list not found. Item does not exist"
            }
            return response, 404

        item = Shoppingitem.query.filter_by(
            uuid=item_id, shoppinglist=list_id).first()

        if not item:
            response = {
                "message": "Item does not exist found in shopping list"
            }
            return response, 404

        item.bought = True
        item.save()
        data = item.serialize()
        item_json = json.dumps(
            data, default=datetimeconverter, sort_keys=True
        )
        response = {
            "message": "Item bought!",
            "item": json.loads(item_json)
        }
        return response, 200

    @token_required
    def delete(self, user_id, list_id, item_id):
        """
            Handle deleting of an item in a shopping list via an id
            Resource Url --> /api/v1/shoppinglist/<list_id>/item/<item_id>
        """
        shoppinglist = Shoppinglist.query.filter_by(
            uuid=list_id, created_by=user_id).first()

        if not shoppinglist:
            response = {
                "message": "Shopping list not found. Item does not exist"
            }
            return response, 404

        item = Shoppingitem.query.filter_by(
            uuid=item_id, shoppinglist=list_id).first()

        if not item:
            response = {
                "message": "Item does not exist found in shopping list"
            }
            return response, 404

        item.delete()
        message = "Item {} deleted!".format(item.name)
        response = {
            "message": message
        }
        return response, 200
