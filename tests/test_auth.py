"""Modeule to test authentication in the application"""
import json

from tests.basetest import TestBase


class AuthTestCase(TestBase):
    """Test authentication namespace"""

    def test_registration(self):
        """Test if registration works correctly"""
        res = self.client.post(
            '/api/v1/auth/register',
            data=self.user_data
        )
        result = json.loads(res.data.decode())
        self.assertEqual(
            result['message'],
            'Registered successfully, please log in.'
        )
        self.assertEqual(res.status_code, 201)

    def test_already_registered(self):
        """Test is users can't be registered more than once"""
        res = self.client.post(
            '/api/v1/auth/register',
            data=self.user_data
        )
        self.assertEqual(res.status_code, 201)
        second_res = self.client.post(
            '/api/v1/auth/register',
            data=self.user_data
        )
        result = json.loads(second_res.data.decode())
        self.assertEqual(second_res.status_code, 202)
        self.assertEqual(
            result['message'],
            "User already exists. Please login."
        )

    def test_user_login(self):
        """Test if a users can login"""
        res = self.client.post(
            '/api/v1/auth/register',
            data=self.user_data
        )
        self.assertEqual(res.status_code, 201)

        login_res = self.client.post(
            '/api/v1/auth/login',
            data=self.user_data_login
        )
        result = json.loads(login_res.data.decode())
        self.assertEqual(result['message'], "You logged in successfully.")
        self.assertEqual(login_res.status_code, 200)
        self.assertTrue(result['token'])

    def test_non_registered_user_login(self):
        """Test if users who are not registered can log in"""
        bad_user = {
            'email': 'bad.user@bad.com',
            'password': 'amabaddie'
        }

        login_res = self.client.post(
            '/api/v1/auth/login',
            data=bad_user
        )
        self.assertEqual(login_res.status_code, 401)
        result = json.loads(login_res.data.decode())
        self.assertEqual(
            result['message'], "Invalid email or password, Please try again")
