from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from services.order_service import OrderService
from services.auth_service import login_required
from models.order import Order
from models.user import User

order_bp = Blueprint('order', __name__)

@order_bp.route('/checkout', methods=['GET'])
@login_required
def checkout():
    cart_info = OrderService.get_cart()
    if not cart_info['items']:
        flash('Your cart is empty. Add items before checkout.', 'warning')
        return redirect(url_for('food.menu'))

    user = User.find_by_id(session['user_id'])
    return render_template('customer/checkout.html', cart=cart_info, user=user)

@order_bp.route('/order/place', methods=['POST'])
@login_required
def place_order():
    cart_info = OrderService.get_cart()
    if not cart_info['items']:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('food.menu'))

    user_id = session['user_id']
    customer_name = request.form.get('customer_name', session.get('user_name', 'Customer'))
    delivery_address = request.form.get('delivery_address', '').strip()

    if not delivery_address:
        flash('Delivery address is required.', 'danger')
        return redirect(url_for('order.checkout'))

    order_id = Order.create(user_id, customer_name, cart_info['items'], delivery_address)
    if order_id:
        OrderService.clear_cart()
        return redirect(url_for('payment.payment_page', order_id=order_id))

    flash('Failed to place order. Please try again.', 'danger')
    return redirect(url_for('order.checkout'))

@order_bp.route('/orders')
@login_required
def order_history():
    user_id = session['user_id']
    orders = Order.get_by_user(user_id)
    return render_template('customer/orders.html', orders=orders)

@order_bp.route('/order/<int:order_id>')
@login_required
def order_details(order_id):
    order = Order.get_by_id(order_id)
    if not order:
        flash('Order not found.', 'danger')
        return redirect(url_for('order.order_history'))

    # Security check: customer can only view own order unless admin
    if session.get('role') != 'admin' and order['user_id'] != session.get('user_id'):
        flash('Unauthorized access to order.', 'danger')
        return redirect(url_for('order.order_history'))

    return render_template('customer/order_details.html', order=order)

@order_bp.route('/receipt/<int:order_id>')
@login_required
def receipt(order_id):
    order = Order.get_by_id(order_id)
    if not order:
        flash('Receipt not found.', 'danger')
        return redirect(url_for('order.order_history'))

    if session.get('role') != 'admin' and order['user_id'] != session.get('user_id'):
        flash('Unauthorized access to receipt.', 'danger')
        return redirect(url_for('order.order_history'))

    return render_template('customer/receipt.html', order=order)
