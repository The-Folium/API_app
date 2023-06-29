import unittest
from flask import Flask
from flask.testing import FlaskClient
from main import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_users(self):
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def test_add_user(self):
        new_user = {'name': 'John', 'email': 'john@example.com'}
        response = self.app.post('/add_user', json=new_user)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content_type, 'application/json')

    def test_delete_user(self):
        user_to_delete = {'name': 'John'}
        response = self.app.delete(f'/delete_user', json=user_to_delete)
        self.assertEqual(response.status_code, 204)

       
if __name__ == '__main__':
    unittest.main()
