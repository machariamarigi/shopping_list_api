from tests.basetest import TestBase
from models import User


class UserTestCase(TestBase):
    """Class to to test the user model"""
    def test_create_user_instance(self):
        user = User(
            username="marigi",
            email="marigi@gm.cm",
            password="cool"
        )
        user.save()
        query_user = User.query.filter_by(email="marigi@gm.cm").first()
        self.assertTrue(query_user == user)

    def test_password_verification(self):
        """test password hash verification"""
        new_user = User(
            username="marigi",
            email="marigi@gm.cm",
            password="cool"
        )
        self.assertTrue(new_user.authenticate_password("cool"))


class ShoppinglistTestCase(TestBase):
    """Class to test the shopping list model"""
    pass


class ShoppingItemTese(TestBase):
    """Class to test the shopping item model"""
    pass