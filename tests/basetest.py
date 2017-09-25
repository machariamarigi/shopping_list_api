"""
    Module containing a TestBase class which other testbases will inherit from
"""
from flask_testing import TestCase

from app import create_app
from api_v1.models import db, User


class TestBase(TestCase):
    """Base class which other tests will inherit from"""

    def create_app(self):
        config_name = 'testing'
        app = create_app(config_name)
        return app

    def setUp(self):
        db.create_all()

        self.user = User(
            username="marigi",
            email="marigi@gm.cm",
            password="cool"
        )

        self.user_data = {
            'username': 'test',
            'email': 'test@test.com',
            'password': 'test_password'
        }

        self.user_data_login = {
            'email': 'test@test.com',
            'password': 'test_password'
        }

        self.shoppinglist = {'name': 'Hardware'}

    def tearDown(self):

        db.session.remove()
        db.drop_all()

    def register_user(
            self,
            username="test",
            email="test@test.com",
            password="test_password"):
        """Method to register a test user"""
        reg_user_data = {
            'username': username,
            'email': email,
            'password': password
        }

        return self.client.post(
            '/api/v1/auth/register',
            data=reg_user_data
        )

    def login_user(self, email="test@test.com", password="test_password"):
        """Method to login a test user"""
        log_user_data = {
            'email': email,
            'password': password
        }

        return self.client.post(
            '/api/v1/auth/login',
            data=log_user_data
        )

    def register_second_user(
            self,
            username="test2",
            email="test2@test.com",
            password="test_password"):
        """Method to register a test user"""
        reg_user_data = {
            'username': username,
            'email': email,
            'password': password
        }

        return self.client.post(
            '/api/v1/auth/register',
            data=reg_user_data
        )

    def login_second_user(
            self, email="test2@test.com", password="test_password"):
        """Method to login a test user"""
        log_user_data = {
            'email': email,
            'password': password
        }

        return self.client.post(
            '/api/v1/auth/login',
            data=log_user_data
        )
