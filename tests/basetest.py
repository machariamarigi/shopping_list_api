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

    def tearDown(self):

        db.session.remove()
        db.drop_all()
