from flask_testing import TestCase

from app import create_app
from models import db, User


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

    def tearDown(self):

        db.session.remove()
        db.drop_all()
