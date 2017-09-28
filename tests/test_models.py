"""Module for testing modles for the API"""
from tests.basetest import TestBase
from api_v1.models import User, Shoppinglist, Shoppingitem


class UserTestCase(TestBase):
    """Class to to test the user model"""

    def test_create_models_instance(self):
        """Test number of users in the users table"""
        self.user.save()
        query_user = User.query.filter_by(email="marigi@gm.cm").first()
        self.assertTrue(query_user == self.user)

    def test_password_verification(self):
        """Test password hash verification"""
        self.assertEqual(self.user.password, self.user.password_hash)
        self.assertTrue(self.user.authenticate_password("cool"))

    def test_delete_models(self):
        """Test deleting from the database"""
        self.user.save()
        query_user = User.query.filter_by(email="marigi@gm.cm").first()
        self.assertTrue(query_user == self.user)
        self.user.delete()
        query_user2 = User.query.filter_by(email="marigi@gm.cm").first()
        self.assertFalse(query_user2 == self.user)

    def test_serialize_models(self):
        """Test dictionary serialization of model objects"""
        serialized_user = self.user.serialize()
        self.assertTrue(serialized_user['username'] == "marigi")

    def test_user_repr(self):
        """Test string representation of the use model"""
        userrepr = repr(self.user)
        self.assertEqual(userrepr, "<User: marigi>")


class ShoppinglistTestCase(TestBase):
    """Class to test the shoppinglist model"""
    def test_shoppinglist_model(self):
        """Test number of shoppinglists in the shoppinglists table"""
        shoppinglist = Shoppinglist(name="Groceries", created_by=None)
        sholi_repr = repr(shoppinglist)
        shoppinglist.save()

        self.assertEqual(Shoppinglist.query.count(), 1)
        self.assertEqual(sholi_repr, "<Shopping List: Groceries>")


class ShoppingitemTestCase(TestBase):
    """Class to test the shopping item model"""
    def test_shopping_item_model(self):
        """Test number of shopping items in the shoppingitems table"""
        item = Shoppingitem(name="Eggplant", quantity=5, shoppinglist=None)
        item_repr = repr(item)
        item.save()

        self.assertEqual(Shoppingitem.query.count(), 1)
        self.assertEqual(item_repr, "<Item: Eggplant>")
