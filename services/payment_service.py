from models.payment import Payment
from models.order import Order

class PaymentService:
    @staticmethod
    def process_demo_payment(order_id, payment_method):
        order = Order.get_by_id(order_id)
        if not order:
            return None, "Order not found"

        transaction_id = Payment.process_payment(order_id, payment_method, order['grand_total'])
        return transaction_id, "Payment Successful"
