import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from database.seed_data import seed_database

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        seed_database()
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    def test_login_success(self):
        response = self.client.post('/login', data={
            'email': 'customer@example.com',
            'password': 'Customer@123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome back', response.data)

    def test_login_failure(self):
        response = self.client.post('/login', data={
            'email': 'customer@example.com',
            'password': 'WrongPassword'
        }, follow_redirects=True)
        self.assertIn(b'Invalid email address or password', response.data)

    def test_register_new_user(self):
        response = self.client.post('/register', data={
            'name': 'Test New User',
            'email': 'testnewuser@example.com',
            'password': 'TestPassword123',
            'confirm_password': 'TestPassword123',
            'phone': '9876543210',
            'address': 'Test Address'
        }, follow_redirects=True)
        self.assertIn(b'Registration successful', response.data)

if __name__ == '__main__':
    unittest.main()
