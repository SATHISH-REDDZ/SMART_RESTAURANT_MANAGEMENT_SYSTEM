import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from database.seed_data import seed_database

class OrdersTestCase(unittest.TestCase):
    def setUp(self):
        seed_database()
        self.app = create_app()
        self.client = self.app.test_client()

    def test_full_order_flow(self):
        # 1. Login
        self.client.post('/login', data={'email': 'customer@example.com', 'password': 'Customer@123'})

        # 2. Add to cart
        self.client.post('/cart/add/1', data={'quantity': 2})

        # 3. Place order
        order_resp = self.client.post('/order/place', data={
            'customer_name': 'Sathish Customer',
            'delivery_address': '123 Test Street'
        }, follow_redirects=True)
        self.assertEqual(order_resp.status_code, 200)

if __name__ == '__main__':
    unittest.main()
