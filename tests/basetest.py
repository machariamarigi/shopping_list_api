# from flask_testing import TestCase
from unittest import TestCase
from app import create_app

from models import db, User


class TestBase(TestCase):
    """Base class which other tests will inherit from"""

    def setUp(self):
        app = create_app('testing')

        self.app_cntx = app.app_context()
        self.app_cntx.push()
        db.drop_all()
        db.create_all()

        self.user = User(
            username="marigi",
            email="marigi@gm.cm",
            password="cool"
        )

    def tearDown(self):
        self.app_cntx.pop()
