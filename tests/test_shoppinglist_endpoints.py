"""Module to test the API's Shopping list endpoints"""

import json

from tests.basetest import TestBase


class ShoppinglistTestCase(TestBase):
    """Class used to test operations on shoppinglists"""

    def test_shoppinglist_creation(self):
        """Test if API can create a shoppinglist"""

        self.get_access_token()

        res = self.client.post(
            '/api/v1/shoppinglists',
            headers=dict(Authorization=self.access_token),
            data=self.shoppinglist
        )
        self.assertEqual(res.status_code, 201)

    def test_shoppinglist_creation_no_token(self):
        "Test if api cannot crate a shoppinglist without a token"
        res = self.client.post(
            '/api/v1/shoppinglists',
            data=self.shoppinglist
        )
        self.assertEqual(res.status_code, 401)

    def test_invalid_token(self):
        """Test if API cannot create a shoppinglist with invalid token"""
        res = self.client.post(
            '/api/v1/shoppinglists',
            headers=dict(Authorization="fdfgdgfg"),
            data=self.shoppinglist
        )
        self.assertEqual(res.status_code, 401)

    def test_bad_shoppinglist_name(self):
        """Test for special characters in shoppinglist names"""

        self.get_access_token()

        bad_shoppinglist = {'name': 'f**/fdgd"%'}
        res = self.client.post(
            '/api/v1/shoppinglists',
            headers=dict(Authorization=self.access_token),
            data=bad_shoppinglist
        )
        self.assertIn(
            'No special characters for shopping list names',
            str(res.data)
        )

    def test_repeat_shoppinglist_name(self):
        """
            Test whether a user can create 2 or more shoppinglists with the
            same name
        """
        self.get_access_token()

        res = self.client.post(
            '/api/v1/shoppinglists',
            headers=dict(Authorization=self.access_token),
            data=self.shoppinglist
        )

        res2 = self.client.post(
            '/api/v1/shoppinglists',
            headers=dict(Authorization=self.access_token),
            data=self.shoppinglist
        )
        self.assertEqual(res2.status_code, 400)

    def test_get_all_shoppinglists(self):
        """Test if API can get all shoppinglists"""
        self.get_access_token()

        res = self.client.post(
            '/api/v1/shoppinglists',
            headers=dict(Authorization=self.access_token),
            data=self.shoppinglist
        )

        res = self.client.get(
            '/api/v1/shoppinglists',
            headers=dict(Authorization=self.access_token)
        )
        self.assertEqual(res.status_code, 200)

    def test_get_query_shoppinglists(self):
        """Test if API can get shoppinglists via a query"""
        self.get_access_token()

        res = self.client.post(
            '/api/v1/shoppinglists',
            headers=dict(Authorization=self.access_token),
            data=self.shoppinglist
        )

        res = self.client.get(
            '/api/v1/shoppinglists?q=hardw',
            headers=dict(Authorization=self.access_token)
        )
        self.assertEqual(res.status_code, 200)

    def test_get_a_shoppinglist_by_id(self):
        """Test if API can get a single shopping list based on a given ID"""
        self.get_access_token()

        post_result = self.client.post(
            '/api/v1/shoppinglists',
            headers=dict(Authorization=self.access_token),
            data=self.shoppinglist
        )
        results = json.loads(post_result.data.decode())
        shoppinglist = results['shoppinglist']
        result = self.client.get(
            '/api/v1/shoppinglist/{}'.format(shoppinglist['uuid']),
            headers=dict(Authorization=self.access_token)
        )
        self.assertEqual(result.status_code, 200)

    def test_nonexisting_shoppinglist(self):
        """Test if API returns 404 for nonexisting shoppinglists"""
        self.get_access_token()

        result = self.client.get(
            '/api/v1/shoppinglist/23',
            headers=dict(Authorization=self.access_token)
        )
        self.assertEqual(result.status_code, 404)

    def test_edit_a_shoppinglist(self):
        """Test if API can edit a shopping list"""
        self.get_access_token()

        post_result = self.client.post(
            '/api/v1/shoppinglists',
            headers=dict(Authorization=self.access_token),
            data=self.shoppinglist
        )
        results = json.loads(post_result.data.decode())
        shoppinglist = results['shoppinglist']

        put_result = self.client.put(
            '/api/v1/shoppinglist/{}'.format(shoppinglist['uuid']),
            headers=dict(Authorization=self.access_token),
            data={'name': 'Hardware 2'}
        )

        result = self.client.get(
            '/api/v1/shoppinglist/{}'.format(shoppinglist['uuid']),
            headers=dict(Authorization=self.access_token)
        )
        self.assertIn('Hardware 2', str(result.data))

    def test_editing_a_shoppinglist_with_a_bad_name(self):
        """
            Test if API cannot edit a shopping list using a name with special
            characters
        """
        self.get_access_token()

        post_result = self.client.post(
            '/api/v1/shoppinglists',
            headers=dict(Authorization=self.access_token),
            data=self.shoppinglist
        )
        results = json.loads(post_result.data.decode())
        shoppinglist = results['shoppinglist']

        put_result = self.client.put(
            '/api/v1/shoppinglist/{}'.format(shoppinglist['uuid']),
            headers=dict(Authorization=self.access_token),
            data={'name': '*&5ffd£'}
        )
        self.assertEqual(put_result.status_code, 400)

    def test_editing_a_shoppinglist_with_existing_name(self):
        """
            Test if API cannot edit a shopping list name to one that already
            exits
        """
        self.get_access_token()

        post_result = self.client.post(
            '/api/v1/shoppinglists',
            headers=dict(Authorization=self.access_token),
            data=self.shoppinglist
        )
        results = json.loads(post_result.data.decode())
        shoppinglist = results['shoppinglist']

        post_result2 = self.client.post(
            '/api/v1/shoppinglists',
            headers=dict(Authorization=self.access_token),
            data={'name': 'groceries'}
        )
        put_result = self.client.put(
            '/api/v1/shoppinglist/{}'.format(shoppinglist['uuid']),
            headers=dict(Authorization=self.access_token),
            data={'name': 'groceries'}
        )
        self.assertEqual(put_result.status_code, 400)

    def test_edit_nonexisting_shoppinglist(self):
        """Test if API returns 404 for nonexisting shoppinglists"""
        self.get_access_token()

        put_result = self.client.put(
            '/api/v1/shoppinglist/33',
            headers=dict(Authorization=self.access_token),
            data={'name': 'Hardware 2'}
        )

        self.assertEqual(put_result.status_code, 404)

    def test_shoppinglist_deletion(self):
        """Test if API can delete a shoppinglist"""
        self.get_access_token()

        post_result = self.client.post(
            '/api/v1/shoppinglists',
            headers=dict(Authorization=self.access_token),
            data=self.shoppinglist
        )
        results = json.loads(post_result.data.decode())
        shoppinglist = results['shoppinglist']

        res = self.client.delete(
            '/api/v1/shoppinglist/{}'.format(shoppinglist['uuid']),
            headers=dict(Authorization=self.access_token)
        )

        result = self.client.get(
            '/api/v1/shoppinglists/1',
            headers=dict(Authorization=self.access_token)
        )
        self.assertEqual(result.status_code, 404)

    def test_delete_nonexiting_shoppinglist(self):
        """Test if API returns 404 for nonexisting shoppinglists"""
        self.get_access_token()

        res = self.client.delete(
            '/api/v1/shoppinglist/1',
            headers=dict(Authorization=self.access_token)
        )

        self.assertEqual(res.status_code, 404)
