from tests.basetest import TestBase
from models import User, Shoppinglist, Shoppingitem


class UserTestCase(TestBase):
    """Class to to test the user model"""

    def test_create_models_instance(self):
        self.user.save()
        query_user = User.query.filter_by(email="marigi@gm.cm").first()
        self.assertTrue(query_user == self.user)

    def test_password_verification(self):
        """test password hash verification"""
        self.assertEquals(self.user.password, self.user.password_hash)
        self.assertTrue(self.user.authenticate_password("cool"))

    def test_delete_models(self):
        self.user.save()
        query_user = User.query.filter_by(email="marigi@gm.cm").first()
        self.assertTrue(query_user == self.user)
        self.user.delete()
        query_user2 = User.query.filter_by(email="marigi@gm.cm").first()
        self.assertFalse(query_user2 == self.user)

    def test_serialize_models(self):
        serialized_user = self.user.serialize()
        self.assertTrue(serialized_user['username'] == "marigi")


class ShoppinglistTestCase(TestBase):
    """Class to test the shoppinglist model"""
    def test_shoppinglist_model(self):
        """Test number of shoppinglists in the shoppinglists table"""
        shoppinglist = Shoppinglist(name="Groceries")
        shoppinglist.save()

        self.assertEqual(Shoppinglist.query.count(), 1)


class ShoppingitemTestCase(TestBase):
    """Class to test the shopping item model"""
    def test_shopping_item_model(self):
        """Test number of shopping items in the shoppingitems table"""
        item = Shoppingitem(item="Eggplant", quantity=5)
        item.save()

        self.assertEqual(Shoppingitem.query.count(), 1)
