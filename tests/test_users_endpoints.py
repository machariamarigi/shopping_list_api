"""Module to test users endpoints"""

from tests.basetest import TestBase


class UsersEndpointsTestCase(TestBase):
    """Class to test operations on users"""
    def test_get_all_users(self):
        """Test if API can get all users"""
        self.get_access_token()

        res = self.client.get(
            '/api/v1/users',
            headers=dict(Authorization=self.access_token)
        )
        self.assertEqual(res.status_code, 200)

    def test_get_all_users_with_search_query(self):
        """Test if API can get all users"""
        self.get_access_token()

        res = self.client.get(
            '/api/v1/users?q=tes',
            headers=dict(Authorization=self.access_token)
        )
        self.assertEqual(res.status_code, 200)

    def test_get_a_single_user(self):
        """Test if API can return a single user"""
        self.get_access_token()

        res = self.client.get(
            '/api/v1/user',
            headers=dict(Authorization=self.access_token)
        )
        self.assertEqual(res.status_code, 200)

    def test_edit_a_single_user(self):
        """Test if API can edit a single user"""
        self.get_access_token()

        user = {
            'username': 'test_user',
            'email': 'test3@test.com',
            'password': 'test_password'
        }

        res = self.client.put(
            'api/v1/user',
            headers=dict(Authorization=self.access_token),
            data=user
        )

        res = self.client.get(
            '/api/v1/user',
            headers=dict(Authorization=self.access_token)
        )
        self.assertIn('test3@test.com', str(res.data))

    def test_edit_a_single_user_with_bad_email(self):
        """Test if API cannot edit a single user with a badly formated email"""
        self.get_access_token()

        bad_user = {
            'username': 'test_user',
            'email': 'testtest.com',
            'password': 'test_password'
        }

        res = self.client.put(
            'api/v1/user',
            headers=dict(Authorization=self.access_token),
            data=bad_user
        )
        self.assertEqual(res.status_code, 400)

    def test_edit_a_single_user_with_bad_username(self):
        """Test if API cannot edit a single user with a badly formated email"""
        self.get_access_token()

        bad_user = {
            'username': ' ',
            'email': 'test@test.com',
            'password': 'test_password'
        }

        res = self.client.put(
            'api/v1/user',
            headers=dict(Authorization=self.access_token),
            data=bad_user
        )
        self.assertEqual(res.status_code, 400)

    def test_editing_a_user_with_existing_name(self):
        """
            Test if API cannot edit user name or to one that already
            exits
        """
        self.get_access_token()

        user = {
            'username': 'test3_user',
            'email': 'test3@test.com',
            'password': 'test_password'
        }

        res = self.client.post(
            '/api/v1/auth/register',
            data=user
        )

        res = self.client.put(
            'api/v1/user',
            headers=dict(Authorization=self.access_token),
            data=user
        )
        self.assertEqual(res.status_code, 400)

    def test_delete_a_shopping_list(self):
        """Test if API can delete a single user"""
        self.get_access_token()

        res = self.client.delete(
            '/api/v1/user',
            headers=dict(Authorization=self.access_token)
        )

        res = self.client.get(
            '/api/v1/user',
            headers=dict(Authorization=self.access_token)
        )
        self.assertNotIn('test@test.com', str(res.data))
