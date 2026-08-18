import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'restaurant.db')

conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    food_item TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    total_price REAL NOT NULL
)
""")

conn.commit()
conn.close()

print("Database created successfully!")