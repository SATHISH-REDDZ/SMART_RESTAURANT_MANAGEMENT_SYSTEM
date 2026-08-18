from flask import session
import sqlite3
from config import Config
from models.food import Food

class OrderService:
    @staticmethod
    def get_cart():
        if 'cart' not in session:
            session['cart'] = {}  # {food_id_str: quantity}
        
        cart_data = session['cart']
        cart_items = []
        subtotal = 0.0

        for food_id_str, qty in cart_data.items():
            food = Food.get_by_id(int(food_id_str))
            if food:
                item_total = food['price'] * qty
                subtotal += item_total
                cart_items.append({
                    'food_id': food['id'],
                    'name': food['name'],
                    'price': food['price'],
                    'image': food['image'],
                    'is_veg': food['is_veg'],
                    'quantity': qty,
                    'item_total': item_total
                })

        tax = round(subtotal * Config.TAX_RATE, 2)
        grand_total = round(subtotal + tax, 2)

        return {
            'cart_items': cart_items,
            'items': cart_items,
            'count': sum(cart_data.values()),
            'subtotal': subtotal,
            'tax': tax,
            'tax_rate_percent': int(Config.TAX_RATE * 100),
            'grand_total': grand_total
        }

    @staticmethod
    def add_to_cart(food_id, quantity=1):
        if 'cart' not in session:
            session['cart'] = {}
        
        cart = session['cart']
        food_id_str = str(food_id)
        if food_id_str in cart:
            cart[food_id_str] += quantity
        else:
            cart[food_id_str] = quantity
        session.modified = True
        return True

    @staticmethod
    def update_cart_quantity(food_id, quantity):
        if 'cart' not in session:
            session['cart'] = {}
        cart = session['cart']
        food_id_str = str(food_id)

        if quantity <= 0:
            if food_id_str in cart:
                del cart[food_id_str]
        else:
            cart[food_id_str] = quantity

        session.modified = True
        return True

    @staticmethod
    def remove_from_cart(food_id):
        if 'cart' not in session:
            return False
        cart = session['cart']
        food_id_str = str(food_id)
        if food_id_str in cart:
            del cart[food_id_str]
            session.modified = True
            return True
        return False

    @staticmethod
    def clear_cart():
        session['cart'] = {}
        session.modified = True
        return True
