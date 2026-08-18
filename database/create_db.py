import sqlite3
import os
import sys

# Add parent directory to sys.path to access config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import Config

def init_db():
    db_path = Config.DB_PATH
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')

    print(f"Initializing database at: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()

    cursor.executescript(schema_sql)
    conn.commit()
    conn.close()
    print("Database tables created successfully!")

if __name__ == '__main__':
    init_db()