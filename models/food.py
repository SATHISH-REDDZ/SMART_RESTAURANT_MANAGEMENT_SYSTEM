import sqlite3
from config import Config

class Food:
    @staticmethod
    def get_db():
        conn = sqlite3.connect(Config.DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def get_all(cls, search_query=None, category_id=None, price_range=None, diet_type=None):
        conn = cls.get_db()
        cursor = conn.cursor()

        sql = """
            SELECT f.*, c.name as category_name
            FROM foods f
            JOIN categories c ON f.category_id = c.id
            WHERE 1=1
        """
        params = []

        if search_query:
            sql += " AND (f.name LIKE ? OR f.description LIKE ?)"
            params.extend([f"%{search_query}%", f"%{search_query}%"])

        if category_id and str(category_id).isdigit() and int(category_id) > 0:
            sql += " AND f.category_id = ?"
            params.append(int(category_id))

        if price_range:
            if price_range == 'under_100':
                sql += " AND f.price < 100"
            elif price_range == '100_200':
                sql += " AND f.price >= 100 AND f.price <= 200"
            elif price_range == '200_500':
                sql += " AND f.price >= 200 AND f.price <= 500"
            elif price_range == 'above_500':
                sql += " AND f.price > 500"

        if diet_type:
            if diet_type == 'veg':
                sql += " AND f.is_veg = 1"
            elif diet_type == 'non_veg':
                sql += " AND f.is_veg = 0"

        sql += " ORDER BY f.id DESC"

        cursor.execute(sql, params)
        foods = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return foods

    @classmethod
    def get_by_id(cls, food_id):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT f.*, c.name as category_name
            FROM foods f
            JOIN categories c ON f.category_id = c.id
            WHERE f.id = ?
        """, (food_id,))
        food = cursor.fetchone()
        conn.close()
        return dict(food) if food else None

    @classmethod
    def create(cls, name, category_id, description, price, image="default_food.jpg", is_available=1, rating=4.5, is_veg=1):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO foods (name, category_id, description, price, image, is_available, rating, is_veg)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, category_id, description, price, image, is_available, rating, is_veg))
        conn.commit()
        food_id = cursor.lastrowid
        conn.close()
        return food_id

    @classmethod
    def update(cls, food_id, name, category_id, description, price, image=None, is_available=1, is_veg=1):
        conn = cls.get_db()
        cursor = conn.cursor()
        if image:
            cursor.execute("""
                UPDATE foods
                SET name = ?, category_id = ?, description = ?, price = ?, image = ?, is_available = ?, is_veg = ?
                WHERE id = ?
            """, (name, category_id, description, price, image, is_available, is_veg, food_id))
        else:
            cursor.execute("""
                UPDATE foods
                SET name = ?, category_id = ?, description = ?, price = ?, is_available = ?, is_veg = ?
                WHERE id = ?
            """, (name, category_id, description, price, is_available, is_veg, food_id))
        conn.commit()
        conn.close()
        return True

    @classmethod
    def toggle_availability(cls, food_id, is_available):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE foods SET is_available = ? WHERE id = ?", (is_available, food_id))
        conn.commit()
        conn.close()
        return True

    @classmethod
    def delete(cls, food_id):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM foods WHERE id = ?", (food_id,))
        conn.commit()
        conn.close()
        return True

    @classmethod
    def get_popular(cls, limit=6):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT f.*, c.name as category_name, COALESCE(SUM(oi.quantity), 0) as total_sold
            FROM foods f
            JOIN categories c ON f.category_id = c.id
            LEFT JOIN order_items oi ON f.id = oi.food_id
            GROUP BY f.id
            ORDER BY total_sold DESC, f.rating DESC
            LIMIT ?
        """, (limit,))
        foods = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return foods
