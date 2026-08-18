import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from database.seed_data import seed_database
from models.food import Food

class FoodTestCase(unittest.TestCase):
    def setUp(self):
        seed_database()
        self.app = create_app()
        self.client = self.app.test_client()

    def test_menu_page(self):
        response = self.client.get('/menu')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Biryani', response.data)

    def test_food_search(self):
        response = self.client.get('/menu?search=biryani')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Biryani', response.data)

    def test_food_details(self):
        foods = Food.get_all()
        if foods:
            food_id = foods[0]['id']
            response = self.client.get(f'/food/{food_id}')
            self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
