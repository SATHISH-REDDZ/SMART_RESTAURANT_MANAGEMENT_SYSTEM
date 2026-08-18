import sqlite3
from config import Config

class Order:
    @staticmethod
    def get_db():
        conn = sqlite3.connect(Config.DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def create(cls, user_id, customer_name, cart_items, delivery_address):
        if not cart_items:
            return None

        subtotal = sum(item['price'] * item['quantity'] for item in cart_items)
        tax = round(subtotal * Config.TAX_RATE, 2)
        grand_total = round(subtotal + tax, 2)

        conn = cls.get_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO orders (user_id, customer_name, total_amount, tax_amount, grand_total, status, payment_status, delivery_address)
            VALUES (?, ?, ?, ?, ?, 'Pending', 'UNPAID', ?)
        """, (user_id, customer_name, subtotal, tax, grand_total, delivery_address))

        order_id = cursor.lastrowid

        for item in cart_items:
            item_subtotal = item['price'] * item['quantity']
            cursor.execute("""
                INSERT INTO order_items (order_id, food_id, food_name, quantity, price, subtotal)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (order_id, item['food_id'], item['name'], item['quantity'], item['price'], item_subtotal))

        conn.commit()
        conn.close()
        return order_id

    @classmethod
    def get_by_id(cls, order_id):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        order = cursor.fetchone()
        if not order:
            conn.close()
            return None

        order_dict = dict(order)
        cursor.execute("SELECT * FROM order_items WHERE order_id = ?", (order_id,))
        order_dict['items'] = [dict(r) for r in cursor.fetchall()]

        cursor.execute("SELECT * FROM payments WHERE order_id = ?", (order_id,))
        pay = cursor.fetchone()
        order_dict['payment'] = dict(pay) if pay else None

        conn.close()
        return order_dict

    @classmethod
    def get_by_user(cls, user_id):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT o.*, COUNT(oi.id) as total_items
            FROM orders o
            LEFT JOIN order_items oi ON o.id = oi.order_id
            WHERE o.user_id = ?
            GROUP BY o.id
            ORDER BY o.order_date DESC
        """, (user_id,))
        orders = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return orders

    @classmethod
    def get_all(cls, status_filter=None):
        conn = cls.get_db()
        cursor = conn.cursor()
        sql = """
            SELECT o.*, u.email as customer_email, COUNT(oi.id) as total_items
            FROM orders o
            JOIN users u ON o.user_id = u.id
            LEFT JOIN order_items oi ON o.id = oi.order_id
            WHERE 1=1
        """
        params = []
        if status_filter and status_filter != 'all':
            sql += " AND o.status = ?"
            params.append(status_filter)

        sql += " GROUP BY o.id ORDER BY o.order_date DESC"
        cursor.execute(sql, params)
        orders = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return orders

    @classmethod
    def update_status(cls, order_id, new_status):
        valid_statuses = ['Pending', 'Confirmed', 'Preparing', 'Ready', 'Completed', 'Cancelled']
        if new_status not in valid_statuses:
            return False
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE orders SET status = ? WHERE id = ?", (new_status, order_id))
        conn.commit()
        conn.close()
        return True

    @classmethod
    def update_payment_status(cls, order_id, payment_status):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE orders SET payment_status = ? WHERE id = ?", (payment_status, order_id))
        conn.commit()
        conn.close()
        return True
