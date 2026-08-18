import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sqlite3
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import Config

class FoodRecommender:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.similarity_matrix = None
        self.food_df = None

    def load_data(self):
        conn = sqlite3.connect(Config.DB_PATH)
        query = """
            SELECT f.id, f.name, f.description, f.price, f.rating, f.is_veg, f.image, c.name as category_name
            FROM foods f
            JOIN categories c ON f.category_id = c.id
            WHERE f.is_available = 1
        """
        self.food_df = pd.read_sql_query(query, conn)
        conn.close()

        if self.food_df.empty:
            return False

        # Build feature text for TF-IDF
        self.food_df['veg_text'] = self.food_df['is_veg'].apply(lambda x: 'Vegetarian Veg' if x == 1 else 'Non-Vegetarian NonVeg Chicken Meat Mutton Fish Egg')
        self.food_df['combined_features'] = (
            self.food_df['name'] + " " +
            self.food_df['category_name'] + " " +
            self.food_df['description'] + " " +
            self.food_df['veg_text']
        )
        return True

    def train(self):
        if not self.load_data() or self.food_df is None or len(self.food_df) == 0:
            return False

        tfidf_matrix = self.vectorizer.fit_transform(self.food_df['combined_features'])
        self.similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
        return True

    def recommend_similar(self, food_id, top_n=4):
        if self.similarity_matrix is None or self.food_df is None:
            self.train()

        if self.food_df is None or food_id not in self.food_df['id'].values:
            # Fallback to top rated items
            return self.get_popular_fallback(top_n)

        # Get index of target food
        idx = self.food_df[self.food_df['id'] == food_id].index[0]
        sim_scores = list(enumerate(self.similarity_matrix[idx]))

        # Sort foods based on similarity score (excluding itself)
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = [score for score in sim_scores if score[0] != idx][:top_n]

        recommended_indices = [score[0] for score in sim_scores]
        recs = self.food_df.iloc[recommended_indices].to_dict('records')
        return recs

    def get_popular_fallback(self, top_n=4):
        if self.food_df is None:
            self.load_data()
        if self.food_df is None or self.food_df.empty:
            return []
        return self.food_df.sort_values(by='rating', ascending=False).head(top_n).to_dict('records')

    def recommend_for_user_history(self, user_ordered_food_ids, top_n=4):
        if not user_ordered_food_ids:
            return self.get_popular_fallback(top_n)

        all_recs = []
        for food_id in user_ordered_food_ids:
            recs = self.recommend_similar(food_id, top_n=2)
            all_recs.extend(recs)

        # Remove duplicates and items user already ordered
        unique_recs = []
        seen = set(user_ordered_food_ids)
        for r in all_recs:
            if r['id'] not in seen:
                seen.add(r['id'])
                unique_recs.append(r)

        if len(unique_recs) < top_n:
            fallback = self.get_popular_fallback(top_n)
            for f in fallback:
                if f['id'] not in seen:
                    seen.add(f['id'])
                    unique_recs.append(f)

        return unique_recs[:top_n]
