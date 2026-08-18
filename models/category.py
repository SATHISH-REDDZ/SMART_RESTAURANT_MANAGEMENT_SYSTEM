import sqlite3
from config import Config

class Category:
    @staticmethod
    def get_db():
        conn = sqlite3.connect(Config.DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def get_all(cls):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT c.*, COUNT(f.id) as food_count FROM categories c LEFT JOIN foods f ON c.id = f.category_id GROUP BY c.id ORDER BY c.name ASC")
        categories = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return categories

    @classmethod
    def get_by_id(cls, category_id):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
        cat = cursor.fetchone()
        conn.close()
        return dict(cat) if cat else None

    @classmethod
    def create(cls, name, description=""):
        conn = cls.get_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO categories (name, description) VALUES (?, ?)", (name, description))
            conn.commit()
            cat_id = cursor.lastrowid
            return cat_id
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()

    @classmethod
    def update(cls, category_id, name, description=""):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE categories SET name = ?, description = ? WHERE id = ?", (name, description, category_id))
        conn.commit()
        conn.close()
        return True

    @classmethod
    def delete(cls, category_id):
        conn = cls.get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        conn.commit()
        conn.close()
        return True
