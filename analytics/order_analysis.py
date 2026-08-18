import pandas as pd
import sqlite3
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import Config

class OrderAnalysis:
    @staticmethod
    def get_connection():
        return sqlite3.connect(Config.DB_PATH)

    @classmethod
    def get_status_breakdown(cls):
        conn = cls.get_connection()
        query = """
            SELECT status, COUNT(*) as count
            FROM orders
            GROUP BY status
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df.to_dict('records')

    @classmethod
    def get_payment_method_breakdown(cls):
        conn = cls.get_connection()
        query = """
            SELECT payment_method, COUNT(*) as count, SUM(amount) as total_amount
            FROM payments
            GROUP BY payment_method
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df.to_dict('records')
