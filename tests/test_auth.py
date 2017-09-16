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
        """Test is a user cannot be registered more than once"""
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
