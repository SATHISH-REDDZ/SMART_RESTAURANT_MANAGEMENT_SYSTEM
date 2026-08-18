from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from services.auth_service import login_required
from services.payment_service import PaymentService
from models.order import Order

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/payment/<int:order_id>')
@login_required
def payment_page(order_id):
    order = Order.get_by_id(order_id)
    if not order:
        flash('Order not found.', 'danger')
        return redirect(url_for('order.order_history'))

    if order['payment_status'] == 'PAID':
        flash('Payment has already been completed for this order.', 'info')
        return redirect(url_for('order.receipt', order_id=order_id))

    return render_template('customer/payment.html', order=order)

@payment_bp.route('/payment/process', methods=['POST'])
@login_required
def process_payment():
    order_id = int(request.form.get('order_id'))
    payment_method = request.form.get('payment_method', 'Demo Payment')

    tx_id, message = PaymentService.process_demo_payment(order_id, payment_method)

    if tx_id:
        flash(f'Payment Successful! Transaction ID: {tx_id}', 'success')
        return redirect(url_for('order.receipt', order_id=order_id))

    flash(f'Payment Failed: {message}', 'danger')
    return redirect(url_for('payment.payment_page', order_id=order_id))
