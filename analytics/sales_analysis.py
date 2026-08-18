import pandas as pd
import sqlite3
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import Config

class SalesAnalysis:
    @staticmethod
    def get_connection():
        return sqlite3.connect(Config.DB_PATH)

    @classmethod
    def get_summary_metrics(cls):
        conn = cls.get_connection()
        
        # Total Customers
        cust_df = pd.read_sql_query("SELECT COUNT(*) as count FROM users WHERE role='customer'", conn)
        total_customers = int(cust_df.iloc[0]['count'])

        # Total Orders
        orders_df = pd.read_sql_query("SELECT COUNT(*) as count, COALESCE(SUM(grand_total), 0) as revenue FROM orders WHERE payment_status='PAID'", conn)
        total_orders = int(orders_df.iloc[0]['count'])
        total_revenue = float(orders_df.iloc[0]['revenue'])

        # Today's Orders & Today's Revenue
        today_df = pd.read_sql_query("SELECT COUNT(*) as count, COALESCE(SUM(grand_total), 0) as revenue FROM orders WHERE DATE(order_date) = DATE('now', 'localtime')", conn)
        todays_orders = int(today_df.iloc[0]['count'])
        todays_revenue = float(today_df.iloc[0]['revenue'])

        # Most popular food
        pop_df = pd.read_sql_query("""
            SELECT food_name, SUM(quantity) as total_qty
            FROM order_items
            GROUP BY food_name
            ORDER BY total_qty DESC
            LIMIT 1
        """, conn)
        most_popular = pop_df.iloc[0]['food_name'] if not pop_df.empty else "N/A"

        conn.close()
        return {
            'total_customers': total_customers,
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'todays_orders': todays_orders,
            'todays_revenue': todays_revenue,
            'most_popular_food': most_popular
        }

    @classmethod
    def get_sales_by_day(cls, limit_days=14):
        conn = cls.get_connection()
        query = """
            SELECT DATE(order_date) as date, SUM(grand_total) as revenue, COUNT(id) as orders_count
            FROM orders
            WHERE payment_status = 'PAID'
            GROUP BY DATE(order_date)
            ORDER BY date ASC
            LIMIT ?
        """
        df = pd.read_sql_query(query, conn, params=(limit_days,))
        conn.close()
        return df.to_dict('records')

    @classmethod
    def get_sales_by_category(cls):
        conn = cls.get_connection()
        query = """
            SELECT c.name as category, SUM(oi.subtotal) as total_sales, SUM(oi.quantity) as items_sold
            FROM order_items oi
            JOIN foods f ON oi.food_id = f.id
            JOIN categories c ON f.category_id = c.id
            JOIN orders o ON oi.order_id = o.id
            WHERE o.payment_status = 'PAID'
            GROUP BY c.name
            ORDER BY total_sales DESC
        """
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df.to_dict('records')

    @classmethod
    def get_top_foods(cls, limit=5):
        conn = cls.get_connection()
        query = """
            SELECT oi.food_name, SUM(oi.quantity) as total_quantity, SUM(oi.subtotal) as total_revenue
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.id
            WHERE o.payment_status = 'PAID'
            GROUP BY oi.food_name
            ORDER BY total_quantity DESC
            LIMIT ?
        """
        df = pd.read_sql_query(query, conn, params=(limit,))
        conn.close()
        return df.to_dict('records')
