import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from database.seed_data import seed_database

class CartTestCase(unittest.TestCase):
    def setUp(self):
        seed_database()
        self.app = create_app()
        self.client = self.app.test_client()

    def test_add_and_view_cart(self):
        with self.client:
            response = self.client.post('/cart/add/1', data={'quantity': 2}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            cart_resp = self.client.get('/cart')
            self.assertEqual(cart_resp.status_code, 200)
            self.assertIn(b'Hyderabadi Chicken Dum Biryani', cart_resp.data)

if __name__ == '__main__':
    unittest.main()
