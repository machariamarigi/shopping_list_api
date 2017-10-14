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

    def test_proper_username_registration(self):
        """
            Test if API rejects users with special characters in their username
        """
        bad_user = {
            'username': '@/*-ffg',
            'email': 'test@test.com',
            'password': 'test_password'
        }

        res = self.client.post(
            '/api/v1/auth/register',
            data=bad_user
        )
        result = json.loads(res.data.decode())
        self.assertIn('No special characters for users names', str(result))

    def test_proper_email_registration(self):
        """
            Test if API rejects users whose emails have improper format
        """
        bad_user = {
            'username': 'test',
            'email': 'testestcom',
            'password': 'test_password'
        }

        res = self.client.post(
            '/api/v1/auth/register',
            data=bad_user
        )
        result = json.loads(res.data.decode())
        self.assertEqual(
            result['message'],
            'Incorrect email format.'
        )

    def test_short_password_registration(self):
        """
            Test if API rejects users whose passwords are too short
        """
        bad_user = {
            'username': 'test',
            'email': 'test@test.com',
            'password': 'test'
        }

        res = self.client.post(
            '/api/v1/auth/register',
            data=bad_user
        )
        result = json.loads(res.data.decode())
        self.assertEqual(
            result['message'],
            'Password too short.'
        )

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
        self.assertIn(
            "Email or username already used. Try",
            result['message']
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
        result = json.loads(login_res.data.decode())
        self.assertEqual(
            result['message'], "Invalid email or password, Please try again")

    def test_password_reset(self):
        """Method to test if API can reset a users password"""
        res = self.client.post(
            '/api/v1/auth/register',
            data=self.user_data
        )
        self.assertEqual(res.status_code, 201)

        login_res = self.client.post(
            '/api/v1/auth/login',
            data=self.user_data_login
        )
        self.assertEqual(login_res.status_code, 200)

        reset_res = self.client.post(
            '/api/v1/auth/reset_password',
            data={'email': 'test@test.com'}
        )

        login_res2 = self.client.post(
            '/api/v1/auth/login',
            data=self.user_data_login
        )
        self.assertEqual(login_res2.status_code, 401)

    def test_password_reset_bad_email(self):
        """
        Method to test if API cannot reset a users
        password with abad email
        """
        res = self.client.post(
            '/api/v1/auth/register',
            data=self.user_data
        )

        login_res = self.client.post(
            '/api/v1/auth/login',
            data=self.user_data_login
        )
        reset_res = self.client.post(
            '/api/v1/auth/reset_password',
            data={'email': 'tes@test.com'}
        )
        self.assertEqual(reset_res.status_code, 400)
