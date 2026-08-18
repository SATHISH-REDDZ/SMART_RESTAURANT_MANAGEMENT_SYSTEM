from flask import Flask, render_template, session
import os
from config import Config

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(Config)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Register Blueprints
    from routes.auth import auth_bp
    from routes.customer import customer_bp
    from routes.food import food_bp
    from routes.cart import cart_bp
    from routes.order import order_bp
    from routes.payment import payment_bp
    from routes.recommendation import recommendation_bp
    from routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(food_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(recommendation_bp)
    app.register_blueprint(admin_bp)

    # Global Context Processor for cart count & session data
    @app.context_processor
    def inject_global_vars():
        from services.order_service import OrderService
        cart = OrderService.get_cart()
        return {
            'cart_count': cart['count'],
            'current_user_name': session.get('user_name'),
            'current_user_role': session.get('role'),
            'is_logged_in': 'user_id' in session
        }

    # Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    return app

app = create_app()

if __name__ == '__main__':
    print("Starting Smart Restaurant Management System...")
    app.run(host='127.0.0.1', port=5000, debug=True)
