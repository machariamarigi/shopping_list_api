"""This module contains the API endpoints in regards to the shopping lists"""
import json

from flask import request
from flask_restplus import Resource
from sqlalchemy import func

from api_v1 import sh_ns
from api_v1.serializers import shoppinglist_model, item_model
from api_v1.models import Shoppinglist, Shoppingitem
from api_v1.helpers import (name_validalidation, datetimeconverter,
                            token_required)
from api_v1.parsers import (shoppinglist_parser, paginate_query_parser,
                            item_parser)


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

        args = shoppinglist_parser.parse_args()
        name = args['name']

        validation_name = name_validalidation(name, "shopping list")
        if validation_name:
            return validation_name

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
    @sh_ns.expect(paginate_query_parser)
    def get(self, user_id):
        """
            Handle getting of all shoppinglists for an authorized user.
            Resource Url --> /api/v1/shoppinglists
        """

        args = paginate_query_parser.parse_args(request)
        search_query = args.get("q")
        page = args.get('page', 1)
        per_page = args.get('limit', 10)

        if search_query:
            shoppinglists = Shoppinglist.query.filter(
                Shoppinglist.name.ilike('%' + search_query + '%'))
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

        shoppinglists = Shoppinglist.query.filter_by(created_by=user_id)
        paginate_shoppinglists = shoppinglists.paginate(page, per_page, True)
        results = []

        for shoppinglist in paginate_shoppinglists.items:
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
    @sh_ns.expect(shoppinglist_model)
    def put(self, user_id, list_id):
        """
            Handle updating of a shoppinglist for an authorized user via an id
            Resource Url --> /api/v1/shoppinglist/<list_id>
        """

        args = shoppinglist_parser.parse_args()
        name = args['name']

        shoppinglist = Shoppinglist.query.filter_by(
            uuid=list_id, created_by=user_id).first()

        if not shoppinglist:
            response = {
                "message": "Shopping list not found"
            }
            return response, 404

        validation_name = name_validalidation(name, "shopping list")
        if validation_name:
            return validation_name

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

        args = item_parser.parse_args()
        name = args['name']
        quantity = args['quantity']

        validation_name = name_validalidation(name, "item")
        if validation_name:
            return validation_name

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
    @sh_ns.expect(paginate_query_parser)
    def get(self, user_id, list_id):
        """
            Handle getting of all items for a shoppinglist.
            Resource Url --> /api/v1/shoppinglist/<int:list_id>/items
        """
        del user_id

        args = paginate_query_parser.parse_args(request)
        search_query = args.get("q")
        page = args.get('page', 1)
        per_page = args.get('limit', 10)

        if search_query:
            items = Shoppingitem.query.filter(
                Shoppingitem.name.ilike('%' + search_query + '%'))
            results = []

            for item in items:
                data = item.serialize()
                item_json = json.dumps(
                    data, default=datetimeconverter, sort_keys=True
                )
                results.append(json.loads(item_json))

            response = {
                "message": "Users shoppinglists found!",
                "shoppinglists": results
            }
            return response, 200

        items = Shoppingitem.query.filter_by(shoppinglist=list_id)
        paginate_items = items.paginate(page, per_page, True)
        results = []

        for item in paginate_items.items:
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
    @sh_ns.expect(item_model)
    def put(self, user_id, list_id, item_id):
        """
            Handle editing of an item in a shopping list via an id
            Resource Url --> /api/v1/shoppinglist/<list_id>/item/<item_id>
        """

        args = item_parser.parse_args()
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

        validation_name = name_validalidation(name, "item")
        if validation_name:
            return validation_name

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
