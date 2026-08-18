import sqlite3
from config import Config

class Review:
    @staticmethod
    def get_db():
        conn = sqlite3.connect(Config.DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def create(cls, user_id, food_id, rating, comment=""):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO reviews (user_id, food_id, rating, comment)
            VALUES (?, ?, ?, ?)
        """, (user_id, food_id, rating, comment))
        conn.commit()

        # Update average rating of food
        cursor.execute("SELECT AVG(rating) FROM reviews WHERE food_id = ?", (food_id,))
        avg_rating = cursor.fetchone()[0]
        if avg_rating:
            cursor.execute("UPDATE foods SET rating = ? WHERE id = ?", (round(avg_rating, 1), food_id))
            conn.commit()

        conn.close()
        return True

    @classmethod
    def get_by_food(cls, food_id):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.*, u.name as user_name
            FROM reviews r
            JOIN users u ON r.user_id = u.id
            WHERE r.food_id = ?
            ORDER BY r.created_at DESC
        """, (food_id,))
        reviews = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return reviews
