"""Module to test the API Shopping Items endpoints"""

import json

from tests.basetest import TestBase


class ShoppinglistTestCase(TestBase):
    """Class used to test operations on shoppinglists"""

    def test_shoppingitem_creation(self):
        """Test is API can create a shopping item in a shopping list"""
        self.create_shoppinglist()

        res = self.client.post(
            '/api/v1/shoppinglist/{}/items'.format(self.shoppinglist_id),
            headers=dict(Authorization=self.access_token),
            data=self.item
        )
        self.assertEqual(res.status_code, 201)

    def test_bad_item_name_quantity(self):
        """
            Test for special characters in item names and non integer quantity
        """

        self.create_shoppinglist()

        bad_item1 = {'name': 'f**/fdgd"%', 'quantity': 2}
        bad_item2 = {'name': 'Hardware', 'quantity': 'fish'}
        self.client.post(
            '/api/v1/shoppinglist/{}/items'.format(self.shoppinglist_id),
            headers=dict(Authorization=self.access_token),
            data=bad_item1
        )

        res2 = self.client.post(
            '/api/v1/shoppinglist/{}/items'.format(self.shoppinglist_id),
            headers=dict(Authorization=self.access_token),
            data=bad_item2
        )

        self.assertEqual(res2.status_code, 400)

    def test_repeat_item_name(self):
        """
            Test whether a user can create 2 or more items with the
            same name in a given shoppinglist
        """
        self.create_shoppinglist()

        self.client.post(
            '/api/v1/shoppinglist/{}/items'.format(self.shoppinglist_id),
            headers=dict(Authorization=self.access_token),
            data=self.item
        )

        res2 = self.client.post(
            '/api/v1/shoppinglist/{}/items'.format(self.shoppinglist_id),
            headers=dict(Authorization=self.access_token),
            data=self.item
        )
        self.assertEqual(res2.status_code, 400)

    def test_get_all_items(self):
        """Test if API can get all items of a shoppinglist"""
        self.create_shoppinglist()

        res = self.client.post(
            '/api/v1/shoppinglist/{}/items'.format(self.shoppinglist_id),
            headers=dict(Authorization=self.access_token),
            data=self.item
        )

        res = self.client.get(
            '/api/v1/shoppinglist/{}/items'.format(self.shoppinglist_id),
            headers=dict(Authorization=self.access_token)
        )
        self.assertEqual(res.status_code, 200)

    def test_get_no_items(self):
        """Test if API can get all items of a shoppinglist"""
        self.create_shoppinglist()

        res = self.client.get(
            '/api/v1/shoppinglist/{}/items'.format(self.shoppinglist_id),
            headers=dict(Authorization=self.access_token)
        )
        self.assertIn('Shopping list has no items', str(res.data))

    def test_get_query_items(self):
        """Test if API can get items of a shoppinglist via a query term"""
        self.create_shoppinglist()

        res = self.client.post(
            '/api/v1/shoppinglist/{}/items'.format(self.shoppinglist_id),
            headers=dict(Authorization=self.access_token),
            data=self.item
        )

        res = self.client.get(
            '/api/v1/shoppinglist/{}/items?q=ham'.format(self.shoppinglist_id),
            headers=dict(Authorization=self.access_token)
        )
        self.assertEqual(res.status_code, 200)

    def test_get_bad_query_items(self):
        """Test if API can get items of a shoppinglist via a query term"""
        self.create_shoppinglist()

        res = self.client.get(
            '/api/v1/shoppinglist/{}/items?q=ham'.format(self.shoppinglist_id),
            headers=dict(Authorization=self.access_token)
        )
        self.assertIn('Shopping list has no items matching ham', str(res.data))

    def test_get_an_item_by_id(self):
        """Test if API can get a single item based on a given ID"""
        self.create_shoppinglist()

        post_result = self.client.post(
            '/api/v1/shoppinglist/{}/items'.format(self.shoppinglist_id),
            headers=dict(Authorization=self.access_token),
            data=self.item
        )
        results = json.loads(post_result.data.decode())
        item = results['item']
        result = self.client.get(
            '/api/v1/shoppinglist/{}/item/{}'.format(
                self.shoppinglist_id, item['uuid']),
            headers=dict(Authorization=self.access_token)
        )
        self.assertEqual(result.status_code, 200)

    def test_nonexisting_item(self):
        """Test if API returns 404 for nonexisting items"""
        self.create_shoppinglist()

        self.client.get(
            '/api/v1/shoppinglist/23/item/1',
            headers=dict(Authorization=self.access_token)
        )

        result2 = self.client.get(
            '/api/v1/shoppinglist/1/item/23',
            headers=dict(Authorization=self.access_token)
        )
        self.assertEqual(result2.status_code, 404)

    def test_edit_an_item(self):
        """Test if API can edit an item in a shopping list"""
        self.create_shoppinglist()

        post_result = self.client.post(
            '/api/v1/shoppinglist/{}/items'.format(self.shoppinglist_id),
            headers=dict(Authorization=self.access_token),
            data=self.item
        )
        results = json.loads(post_result.data.decode())
        item = results['item']

        self.client.put(
            '/api/v1/shoppinglist/{}/item/{}'.format(
                self.shoppinglist_id, item['uuid']),
            headers=dict(Authorization=self.access_token),
            data={'name': 'Mjolner', 'quantity': 12}
        )

        result = self.client.get(
            '/api/v1/shoppinglist/{}/item/{}'.format(
                self.shoppinglist_id, item['uuid']),
            headers=dict(Authorization=self.access_token)
        )
        self.assertIn('Mjolner', str(result.data))

    def test_edit_an_item_with_bad_name(self):
        """Test if API can edit a shopping list"""
        self.create_shoppinglist()

        post_result = self.client.post(
            '/api/v1/shoppinglist/{}/items'.format(self.shoppinglist_id),
            headers=dict(Authorization=self.access_token),
            data=self.item
        )
        results = json.loads(post_result.data.decode())
        item = results['item']

        put_result = self.client.put(
            '/api/v1/shoppinglist/{}/item/{}'.format(
                self.shoppinglist_id, item['uuid']),
            headers=dict(Authorization=self.access_token),
            data={'name': '*&5ffd£', 'quantity': 1}
        )
        self.assertIn(
            'No special characters for item names',
            str(put_result.data)
        )

    def test_editing_an_item_with_existing_name(self):
        """
            Test if API cannot edit an item name to one that already
            exits in the shopping list
        """
        self.create_shoppinglist()

        post_result = self.client.post(
            '/api/v1/shoppinglist/{}/items'.format(self.shoppinglist_id),
            headers=dict(Authorization=self.access_token),
            data=self.item
        )
        results = json.loads(post_result.data.decode())
        item = results['item']

        post_result2 = self.client.post(
            '/api/v1/shoppinglist/{}/items'.format(self.shoppinglist_id),
            headers=dict(Authorization=self.access_token),
            data={'name': 'nails', 'quantity': 50}
        )
        self.assertEqual(post_result2.status_code, 201)
        put_result = self.client.put(
            '/api/v1/shoppinglist/{}/item/{}'.format(
                self.shoppinglist_id, item['uuid']),
            headers=dict(Authorization=self.access_token),
            data={'name': 'nails', 'quantity': 12}
        )
        self.assertEqual(put_result.status_code, 400)

    def test_edit_nonexisting_item(self):
        """Test if API returns 404 for nonexisting items"""
        self.create_shoppinglist()

        self.client.put(
            '/api/v1/shoppinglist/23/item/1',
            headers=dict(Authorization=self.access_token),
            data=self.item
        )

        result2 = self.client.put(
            '/api/v1/shoppinglist/1/item/23',
            headers=dict(Authorization=self.access_token),
            data=self.item
        )
        self.assertEqual(result2.status_code, 404)

    def test_buying_an_item_by_id(self):
        """Test if API can get a single item based on a given ID"""
        self.create_shoppinglist()

        post_result = self.client.post(
            '/api/v1/shoppinglist/{}/items'.format(self.shoppinglist_id),
            headers=dict(Authorization=self.access_token),
            data=self.item
        )
        results = json.loads(post_result.data.decode())
        item = results['item']
        result = self.client.patch(
            '/api/v1/shoppinglist/{}/item/{}'.format(
                self.shoppinglist_id, item['uuid']),
            headers=dict(Authorization=self.access_token)
        )
        results = json.loads(result.data.decode())
        item = results['item']
        self.assertEqual(item['bought'], True)

    def test_buy_nonexisting_item(self):
        """Test if API returns 404 for nonexisting items"""
        self.create_shoppinglist()

        self.client.patch(
            '/api/v1/shoppinglist/23/item/1',
            headers=dict(Authorization=self.access_token)
        )

        result2 = self.client.patch(
            '/api/v1/shoppinglist/1/item/23',
            headers=dict(Authorization=self.access_token)
        )
        self.assertEqual(result2.status_code, 404)

    def test_item_deletion(self):
        """Test if API can delete items in a shopping list"""
        self.create_shoppinglist()

        post_result = self.client.post(
            '/api/v1/shoppinglist/{}/items'.format(self.shoppinglist_id),
            headers=dict(Authorization=self.access_token),
            data=self.item
        )
        results = json.loads(post_result.data.decode())
        item = results['item']

        self.client.delete(
            '/api/v1/shoppinglist/{}/item/{}'.format(
                self.shoppinglist_id, item['uuid']),
            headers=dict(Authorization=self.access_token)
        )

        result = self.client.get(
            '/api/v1/shoppinglist/{}/item/{}'.format(
                self.shoppinglist_id, item['uuid']),
            headers=dict(Authorization=self.access_token)
        )
        self.assertEqual(result.status_code, 404)

    def test_delete_nonexiting_item(self):
        """Test if API returns 404 for nonexisting shoppinglists"""
        self.create_shoppinglist()

        self.client.delete(
            '/api/v1/shoppinglist/23/item/1',
            headers=dict(Authorization=self.access_token)
        )

        result2 = self.client.delete(
            '/api/v1/shoppinglist/1/item/23',
            headers=dict(Authorization=self.access_token)
        )
        self.assertEqual(result2.status_code, 404)
