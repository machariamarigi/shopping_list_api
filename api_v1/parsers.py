"""Module that contains request parsers for the API"""
from flask_restplus import reqparse

registration_parser = reqparse.RequestParser()
registration_parser.add_argument(
    'username',
    required=True,
    help='required and must be a string'
)
registration_parser.add_argument(
    'email',
    required=True,
    help='required and must be a string'
)
registration_parser.add_argument(
    'password',
    required=True,
    help='required and must be a string'
)

login_parser = reqparse.RequestParser()
login_parser.add_argument(
    'email',
    required=True,
    help='required and must be a string'
)
login_parser.add_argument(
    'password',
    required=True,
    help='required and must be a string'
)

password_reset = reqparse.RequestParser()
password_reset.add_argument(
    'email',
    required=True,
    help='require and must be a string'
)

shoppinglist_parser = reqparse.RequestParser()
shoppinglist_parser.add_argument(
    'name',
    required=True,
    help="Required and must be a string"
)

item_parser = reqparse.RequestParser()
item_parser.add_argument(
    'name',
    required=True,
    type=str,
    help="Required and must be a string"
)
item_parser.add_argument(
    'quantity',
    required=True,
    type=int,
    help="Required and must be an integer"
)

paginate_query_parser = reqparse.RequestParser()
paginate_query_parser.add_argument(
    'q', type=str, required=False, help="Search for"
)
paginate_query_parser.add_argument(
    'page', type=int, required=False, help="pages of results"
)
paginate_query_parser.add_argument(
    'limit', type=int, required=False, help="limit per page"
)

user_parser = reqparse.RequestParser()
user_parser.add_argument(
    'username',
    required=True,
    help='required and must be a string'
)
user_parser.add_argument(
    'email',
    required=True,
    help='Required and must be a string'
)
