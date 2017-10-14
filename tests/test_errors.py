"""Module for testing the running of the API"""
import json

from flask import abort

from .basetest import TestBase


class TestErrors(TestBase):
    """Test error codes and ensure they return json information"""

    def test_403(self):
        """Test general forbidden"""
        @self.app.route('/403')
        def forbidden_error():
            abort(403)

        response = self.client.get('/403')
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['error'] == 'forbidden')

    def test_404(self):
        """Test general not found"""
        response = self.client.get('/badurl')
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['error'] == 'not found')

    def test_500(self):
        """Test general server errors"""
        @self.app.route('/500')
        def server_error():
            """Raise server error"""
            abort(500)
        response = self.client.get('/500')
        self.assertTrue(response.status_code == 500)
