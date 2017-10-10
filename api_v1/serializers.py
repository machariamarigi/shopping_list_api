"""Module containing resplus models used in the API"""
from flask_restplus import fields

from api_v1 import auth, sh_ns

register_args_model = auth.model(
    'registration_args',
    {
        'email': fields.String(required=True, default="user@example.com"),
        'password': fields.String(required=True, default="password_example"),
        'username': fields.String(required=True, default="user_example")
    }
)

login_args_model = auth.model(
    'login_args_model',
    {
        'email': fields.String(required=True, default="user@example.com"),
        'password': fields.String(required=True, default="password_example")
    }
)

password_reset_args_model = auth.model(
    'password_rest_args_model',
    {
        'email': fields.String(required=True, default="user@example.com")
    }
)

shoppinglist_model = sh_ns.model('ShoppingList', {
    'name': fields.String(required=True, default="Groceries")
})

item_model = sh_ns.model(
    'Item', {
        'name': fields.String(required=True, default="Carrots"),
        'quantity': fields.Integer(required=True, default=1)
    }
)

user_model = sh_ns.model(
    'user',
    {
        'email': fields.String(required=True, default="user@example.com"),
        'username': fields.String(required=True, default="user_example")
    }
)
