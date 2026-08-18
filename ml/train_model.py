import sqlite3
import os
import sys
import joblib

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import Config
from ml.recommender import FoodRecommender

def train_and_cache_recommendations():
    print("Training ML Recommendation Model...")
    recommender = FoodRecommender()
    success = recommender.train()

    if not success:
        print("Failed to train model: dataset empty or missing.")
        return

    # Save model pkl
    model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
    joblib.dump(recommender, model_path)
    print(f"ML Model saved to {model_path}")

    # Populate SQLite recommendations cache
    conn = sqlite3.connect(Config.DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM recommendations")
    
    for food_id in recommender.food_df['id']:
        recs = recommender.recommend_similar(food_id, top_n=5)
        for rank, r in enumerate(recs, start=1):
            score = 1.0 - (rank * 0.1)
            cursor.execute("""
                INSERT INTO recommendations (food_id, recommended_food_id, similarity_score)
                VALUES (?, ?, ?)
            """, (food_id, r['id'], score))

    conn.commit()
    conn.close()
    print("Recommendations cache table successfully populated!")

if __name__ == '__main__':
    train_and_cache_recommendations()
