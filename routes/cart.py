from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from services.order_service import OrderService

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart')
def view_cart():
    cart_info = OrderService.get_cart()
    return render_template('customer/cart.html', cart=cart_info)

@cart_bp.route('/cart/add/<int:food_id>', methods=['POST', 'GET'])
def add_to_cart(food_id):
    quantity = int(request.form.get('quantity', 1))
    OrderService.add_to_cart(food_id, quantity)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
        cart_info = OrderService.get_cart()
        return jsonify({'success': True, 'cart_count': cart_info['count'], 'message': 'Item added to cart!'})

    flash('Item added to shopping cart!', 'success')
    return redirect(request.referrer or url_for('food.menu'))

@cart_bp.route('/cart/update', methods=['POST'])
def update_cart():
    food_id = int(request.form.get('food_id'))
    quantity = int(request.form.get('quantity'))

    OrderService.update_cart_quantity(food_id, quantity)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
        cart_info = OrderService.get_cart()
        return jsonify({'success': True, 'cart': cart_info})

    flash('Cart updated successfully.', 'success')
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/cart/remove/<int:food_id>')
def remove_from_cart(food_id):
    OrderService.remove_from_cart(food_id)
    flash('Item removed from cart.', 'info')
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/cart/clear')
def clear_cart():
    OrderService.clear_cart()
    flash('Cart cleared.', 'info')
    return redirect(url_for('cart.view_cart'))
