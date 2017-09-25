"""Modeule to test the API's endpoints"""

import json

from tests.basetest import TestBase


class ShoppingTestCase(TestBase):
    """Class used to test operations on shoppinglists"""

    def test_shoppinglist_creation(self):
        """Test if API can create a shoppinglist"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['token']
        res = self.client.post(
            '/api/v1/shoppinglists',
            headers=dict(Authorization=access_token),
            data=self.shoppinglist
        )
        self.assertEqual(res.status_code, 201)
        self.assertIn('Hardware', str(res.data))

    def test_invalid_token(self):
        """Test if API cannot create a shoppinglist with invalid token"""
        res = self.client.post(
            '/api/v1/shoppinglists',
            headers=dict(Authorization="fdfgdgfg"),
            data=self.shoppinglist
        )
        self.assertEqual(res.status_code, 401)
        self.assertIn('Invalid token. Please register or login', str(res.data))

    def test_expired_token(self):
        """Test if API cannot create a shoppinglist with expired token"""
        expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" \
            ".eyJleHAiOjE1MDYzNDMyMzIsImlhdCI6MTUwNjM0MjkzMiwic3V" \
            "iIjoxfQ.gUlwxJEfz6gAqohBZJ_eRpvlNn0ZvUT4vQ8MciZSyzU"
        res = self.client.post(
            '/api/v1/shoppinglists',
            headers=dict(Authorization=expired_token),
            data=self.shoppinglist
        )
        self.assertEqual(res.status_code, 401)
        self.assertIn(
            'Expired token. Please login to get a new token', str(res.data))

    def test_bad_shoppinglist_name(self):
        """Test for special characters in shoppinglist names"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['token']
        bad_shoppinglist = {'name': 'f**/fdgd"%'}
        res = self.client.post(
            '/api/v1/shoppinglists',
            headers=dict(Authorization=access_token),
            data=bad_shoppinglist
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn(
            'No special characters for shopping list names',
            str(res.data)
        )

    def test_repeat_shoppinglist_name(self):
        """
            Test whether a user can create 2 or more shoppinglists with the
            same name
        """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['token']
        res = self.client.post(
            '/api/v1/shoppinglists',
            headers=dict(Authorization=access_token),
            data=self.shoppinglist
        )
        self.assertEqual(res.status_code, 201)

        res2 = self.client.post(
            '/api/v1/shoppinglists',
            headers=dict(Authorization=access_token),
            data=self.shoppinglist
        )
        self.assertEqual(res2.status_code, 400)
        self.assertIn(
            'Shopping list already exists!',
            str(res2.data)
        )

    def test_get_all_shoppinglists(self):
        """Test if API can get all shoppinglist"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['token']
        res = self.client.post(
            '/api/v1/shoppinglists',
            headers=dict(Authorization=access_token),
            data=self.shoppinglist
        )
        self.assertEqual(res.status_code, 201)

        res = self.client.get(
            '/api/v1/shoppinglists',
            headers=dict(Authorization=access_token)
        )
        self.assertEqual(res.status_code, 200)
        self.assertIn('Hardware', str(res.data))

    def test_get_a_shoppinglist_by_id(self):
        """Test if API can get a single shopping list based on a given ID"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['token']

        post_result = self.client.post(
            '/api/v1/shoppinglists',
            headers=dict(Authorization=access_token),
            data=self.shoppinglist
        )
        self.assertEqual(post_result.status_code, 201)
        results = json.loads(post_result.data.decode())
        shoppinglist = results['shoppinglist']
        result = self.client.get(
            '/api/v1/shoppinglist/{}'.format(shoppinglist['uuid']),
            headers=dict(Authorization=access_token)
        )
        self.assertEqual(result.status_code, 200)
        self.assertIn('Hardware', str(result.data))

    def test_nonexisting_shoppinglist(self):
        """Test if API returns 404 for nonexisting shoppinglists"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['token']

        result = self.client.get(
            '/api/v1/shoppinglist/23',
            headers=dict(Authorization=access_token)
        )
        self.assertEqual(result.status_code, 404)
        self.assertIn('Shopping list not found', str(result.data))

    def test_edit_a_shoppinglist(self):
        """Test if API can edit a shopping list"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['token']

        post_result = self.client.post(
            '/api/v1/shoppinglists',
            headers=dict(Authorization=access_token),
            data=self.shoppinglist
        )
        self.assertEqual(post_result.status_code, 201)
        results = json.loads(post_result.data.decode())
        shoppinglist = results['shoppinglist']

        put_result = self.client.put(
            '/api/v1/shoppinglist/{}'.format(shoppinglist['uuid']),
            headers=dict(Authorization=access_token),
            data={'name': 'Hardware 2'}
        )
        self.assertEqual(put_result.status_code, 200)

        result = self.client.get(
            '/api/v1/shoppinglist/{}'.format(shoppinglist['uuid']),
            headers=dict(Authorization=access_token)
        )
        self.assertIn('Hardware 2', str(result.data))

    def test_editing_a_shoppinglist_with_a_bad_name(self):
        """Test if API can edit a shopping list"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['token']

        post_result = self.client.post(
            '/api/v1/shoppinglists',
            headers=dict(Authorization=access_token),
            data=self.shoppinglist
        )
        self.assertEqual(post_result.status_code, 201)
        results = json.loads(post_result.data.decode())
        shoppinglist = results['shoppinglist']

        put_result = self.client.put(
            '/api/v1/shoppinglist/{}'.format(shoppinglist['uuid']),
            headers=dict(Authorization=access_token),
            data={'name': '*&5ffd£'}
        )
        self.assertEqual(put_result.status_code, 400)
        self.assertIn(
            'No special characters for shopping list names',
            str(put_result.data)
        )

    def test_editing_a_shoppinglist_with_existing_name(self):
        """
            Test if API cannot edit a shopping list name to one that already
            exits
        """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['token']
        post_result = self.client.post(
            '/api/v1/shoppinglists',
            headers=dict(Authorization=access_token),
            data=self.shoppinglist
        )
        self.assertEqual(post_result.status_code, 201)
        results = json.loads(post_result.data.decode())
        shoppinglist = results['shoppinglist']

        post_result2 = self.client.post(
            '/api/v1/shoppinglists',
            headers=dict(Authorization=access_token),
            data={'name': 'groceries'}
        )
        self.assertEqual(post_result2.status_code, 201)
        put_result = self.client.put(
            '/api/v1/shoppinglist/{}'.format(shoppinglist['uuid']),
            headers=dict(Authorization=access_token),
            data={'name': 'groceries'}
        )
        self.assertEqual(put_result.status_code, 400)

    def test_edit_nonexisting_shoppinglist(self):
        """Test if API returns 404 for nonexisting shoppinglists"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['token']

        put_result = self.client.put(
            '/api/v1/shoppinglist/33',
            headers=dict(Authorization=access_token),
            data={'name': 'Hardware 2'}
        )

        self.assertEqual(put_result.status_code, 404)
        self.assertIn('Shopping list not found', str(put_result.data))

    def test_shoppinglist_deletion(self):
        """Test if API can delete a shoppinglist"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['token']

        post_result = self.client.post(
            '/api/v1/shoppinglists',
            headers=dict(Authorization=access_token),
            data=self.shoppinglist
        )
        self.assertEqual(post_result.status_code, 201)
        results = json.loads(post_result.data.decode())
        shoppinglist = results['shoppinglist']

        res = self.client.delete(
            '/api/v1/shoppinglist/{}'.format(shoppinglist['uuid']),
            headers=dict(Authorization=access_token)
        )
        self.assertEqual(res.status_code, 200)

        result = self.client.get(
            '/api/v1/shoppinglists/1',
            headers=dict(Authorization=access_token)
        )
        self.assertEqual(result.status_code, 404)

    def test_delete_nonexiting_shoppinglist(self):
        """Test if API returns 404 for nonexisting shoppinglists"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['token']

        res = self.client.delete(
            '/api/v1/shoppinglist/1',
            headers=dict(Authorization=access_token)
        )

        self.assertEqual(res.status_code, 404)
        self.assertIn('Shopping list not found', str(res.data))
