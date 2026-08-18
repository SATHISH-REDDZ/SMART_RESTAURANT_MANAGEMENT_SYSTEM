from flask import Flask, render_template, request
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, '..', 'HTML')
DB_PATH = os.path.join(BASE_DIR, '..', 'database', 'restaurant.db')

app = Flask(__name__, template_folder=TEMPLATE_DIR)

@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/menu')
def menu():
    return render_template('Menu.html')

@app.route('/about')
def about():
    return render_template('About.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/order')
def order():
    return render_template('order.html')

@app.route('/save_order', methods=['POST'])
def save_order():
    try:
        customer_name = request.form.get('customer_name')
        food_item = request.form.get('food_item')
        quantity = request.form.get('quantity')
        total_price = request.form.get('total_price')

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO orders
            (customer_name, food_item, quantity, total_price)
            VALUES (?, ?, ?, ?)
        """, (customer_name, food_item, quantity, total_price))

        conn.commit()
        conn.close()

        return "Order Saved Successfully!"

    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)