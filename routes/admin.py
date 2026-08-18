from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from services.auth_service import admin_required
from models.food import Food
from models.category import Category
from models.order import Order
from models.user import User
from models.payment import Payment
from analytics.sales_analysis import SalesAnalysis
from analytics.reports import AnalyticsReport

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    metrics = SalesAnalysis.get_summary_metrics()
    recent_orders = Order.get_all()[:5]
    top_foods = SalesAnalysis.get_top_foods(limit=5)
    sales_by_day = SalesAnalysis.get_sales_by_day(limit_days=7)

    return render_template('admin/dashboard.html',
                           metrics=metrics,
                           recent_orders=recent_orders,
                           top_foods=top_foods,
                           sales_by_day=sales_by_day)

@admin_bp.route('/foods')
@admin_required
def foods():
    foods_list = Food.get_all()
    categories = Category.get_all()
    return render_template('admin/foods.html', foods=foods_list, categories=categories)

@admin_bp.route('/foods/add', methods=['GET', 'POST'])
@admin_required
def add_food():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        category_id = request.form.get('category_id')
        description = request.form.get('description', '').strip()
        price = request.form.get('price', 0)
        image = request.form.get('image', '').strip() or 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500'
        is_veg = int(request.form.get('is_veg', 1))
        is_available = int(request.form.get('is_available', 1))

        if not name or not category_id or not price:
            flash('Food name, category, and price are required.', 'warning')
            return redirect(url_for('admin.add_food'))

        Food.create(name, category_id, description, float(price), image, is_available=is_available, is_veg=is_veg)
        flash(f'Food item "{name}" added successfully!', 'success')
        return redirect(url_for('admin.foods'))

    categories = Category.get_all()
    return render_template('admin/add_food.html', categories=categories)

@admin_bp.route('/foods/edit/<int:food_id>', methods=['GET', 'POST'])
@admin_required
def edit_food(food_id):
    food = Food.get_by_id(food_id)
    if not food:
        flash('Food item not found.', 'danger')
        return redirect(url_for('admin.foods'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        category_id = request.form.get('category_id')
        description = request.form.get('description', '').strip()
        price = float(request.form.get('price', 0))
        image = request.form.get('image', '').strip()
        is_veg = int(request.form.get('is_veg', 1))
        is_available = int(request.form.get('is_available', 1))

        Food.update(food_id, name, category_id, description, price, image=image if image else None, is_available=is_available, is_veg=is_veg)
        flash(f'Food item "{name}" updated successfully.', 'success')
        return redirect(url_for('admin.foods'))

    categories = Category.get_all()
    return render_template('admin/edit_food.html', food=food, categories=categories)

@admin_bp.route('/foods/delete/<int:food_id>')
@admin_required
def delete_food(food_id):
    Food.delete(food_id)
    flash('Food item deleted.', 'info')
    return redirect(url_for('admin.foods'))

@admin_bp.route('/foods/toggle/<int:food_id>')
@admin_required
def toggle_food_status(food_id):
    food = Food.get_by_id(food_id)
    if food:
        new_status = 0 if food['is_available'] == 1 else 1
        Food.toggle_availability(food_id, new_status)
        flash('Food availability updated.', 'success')
    return redirect(url_for('admin.foods'))

@admin_bp.route('/categories', methods=['GET', 'POST'])
@admin_required
def categories():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()

        if name:
            res = Category.create(name, description)
            if res:
                flash(f'Category "{name}" created.', 'success')
            else:
                flash('Category already exists.', 'warning')
        return redirect(url_for('admin.categories'))

    categories_list = Category.get_all()
    return render_template('admin/categories.html', categories=categories_list)

@admin_bp.route('/categories/delete/<int:cat_id>')
@admin_required
def delete_category(cat_id):
    Category.delete(cat_id)
    flash('Category deleted.', 'info')
    return redirect(url_for('admin.categories'))

@admin_bp.route('/orders')
@admin_required
def orders():
    status_filter = request.args.get('status', 'all')
    orders_list = Order.get_all(status_filter=status_filter)
    return render_template('admin/orders.html', orders=orders_list, current_filter=status_filter)

@admin_bp.route('/order/<int:order_id>/update', methods=['POST'])
@admin_required
def update_order_status(order_id):
    new_status = request.form.get('status')
    Order.update_status(order_id, new_status)
    flash(f'Order #{order_id} status updated to {new_status}.', 'success')
    return redirect(url_for('admin.orders'))

@admin_bp.route('/customers')
@admin_required
def customers():
    customers_list = User.get_all_customers()
    return render_template('admin/customers.html', customers=customers_list)

@admin_bp.route('/analytics')
@admin_required
def analytics():
    report = AnalyticsReport.generate_full_admin_report()
    return render_template('admin/analytics.html', report=report)

@admin_bp.route('/reports')
@admin_required
def reports():
    report = AnalyticsReport.generate_full_admin_report()
    payments = Payment.get_all()
    return render_template('admin/reports.html', report=report, payments=payments)
