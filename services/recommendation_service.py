from ml.recommender import FoodRecommender
from models.food import Food
import sqlite3
from config import Config

class RecommendationService:
    _recommender = None

    @classmethod
    def get_recommender(cls):
        if cls._recommender is None:
            cls._recommender = FoodRecommender()
            cls._recommender.train()
        return cls._recommender

    @classmethod
    def get_recommendations_for_food(cls, food_id, top_n=4):
        rec_engine = cls.get_recommender()
        recs = rec_engine.recommend_similar(food_id, top_n=top_n)
        return recs

    @classmethod
    def get_recommendations_for_user(cls, user_id, top_n=4):
        conn = sqlite3.connect(Config.DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT oi.food_id
            FROM orders o
            JOIN order_items oi ON o.id = oi.order_id
            WHERE o.user_id = ?
            ORDER BY o.order_date DESC
            LIMIT 5
        """, (user_id,))
        ordered_food_ids = [r[0] for r in cursor.fetchall()]
        conn.close()

        rec_engine = cls.get_recommender()
        recs = rec_engine.recommend_for_user_history(ordered_food_ids, top_n=top_n)
        return recs

    @classmethod
    def get_popular_recommendations(cls, top_n=6, limit=None):
        num = limit if limit is not None else top_n
        return Food.get_popular(limit=num)
