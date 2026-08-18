import os
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'smart-restaurant-secret-key-default-2026')
    DB_PATH = os.path.join(BASE_DIR, os.environ.get('DATABASE_PATH', 'database/restaurant.db'))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    TAX_RATE = float(os.environ.get('TAX_RATE', 0.05))  # 5% tax by default
    REASONABLE_PRICE_THRESHOLD = 500
