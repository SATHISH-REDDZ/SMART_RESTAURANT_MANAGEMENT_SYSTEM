import sqlite3
import random
import string
from config import Config

class Payment:
    @staticmethod
    def get_db():
        conn = sqlite3.connect(Config.DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def process_payment(cls, order_id, payment_method, amount):
        tx_id = f"DEMO{''.join(random.choices(string.ascii_uppercase + string.digits, k=6))}"
        conn = cls.get_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO payments (order_id, payment_method, transaction_id, amount, status)
            VALUES (?, ?, ?, ?, 'PAID')
        """, (order_id, payment_method, tx_id, amount))

        cursor.execute("""
            UPDATE orders SET payment_status = 'PAID', status = 'Confirmed' WHERE id = ?
        """, (order_id,))

        conn.commit()
        conn.close()
        return tx_id

    @classmethod
    def get_by_order(cls, order_id):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM payments WHERE order_id = ?", (order_id,))
        pay = cursor.fetchone()
        conn.close()
        return dict(pay) if pay else None

    @classmethod
    def get_all(cls):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.*, o.customer_name, o.grand_total
            FROM payments p
            JOIN orders o ON p.order_id = o.id
            ORDER BY p.payment_date DESC
        """)
        payments = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return payments
