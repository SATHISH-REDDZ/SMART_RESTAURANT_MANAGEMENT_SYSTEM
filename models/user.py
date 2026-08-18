import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

class User:
    @staticmethod
    def get_db():
        conn = sqlite3.connect(Config.DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def create(cls, name, email, password, phone="", address="", role="customer"):
        hashed_password = generate_password_hash(password)
        conn = cls.get_db()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO users (name, email, password, phone, address, role)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, email, hashed_password, phone, address, role))
            conn.commit()
            user_id = cursor.lastrowid
            return user_id
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()

    @classmethod
    def find_by_email(cls, email):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()
        return dict(user) if user else None

    @classmethod
    def find_by_id(cls, user_id):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()
        return dict(user) if user else None

    @classmethod
    def update_profile(cls, user_id, name, phone, address):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users SET name = ?, phone = ?, address = ? WHERE id = ?
        """, (name, phone, address, user_id))
        conn.commit()
        conn.close()
        return True

    @classmethod
    def verify_password(cls, stored_password_hash, entered_password):
        return check_password_hash(stored_password_hash, entered_password)

    @classmethod
    def get_all_customers(cls):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.*, COUNT(o.id) as total_orders, COALESCE(SUM(o.grand_total), 0) as total_spent
            FROM users u
            LEFT JOIN orders o ON u.id = o.user_id
            WHERE u.role = 'customer'
            GROUP BY u.id
            ORDER BY u.created_at DESC
        """)
        users = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return users
