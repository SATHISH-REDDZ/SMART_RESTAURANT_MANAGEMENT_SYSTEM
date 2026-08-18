from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.food import Food
from models.category import Category
from models.user import User
from services.auth_service import login_required
from services.recommendation_service import RecommendationService

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/')
def home():
    popular_foods = RecommendationService.get_popular_recommendations(limit=6)
    categories = Category.get_all()
    user_id = session.get('user_id')
    personalized_recs = []

    if user_id:
        personalized_recs = RecommendationService.get_recommendations_for_user(user_id, top_n=4)
    else:
        personalized_recs = popular_foods[:4]

    return render_template('customer/home.html', 
                           popular_foods=popular_foods, 
                           categories=categories, 
                           recommendations=personalized_recs)

@customer_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user_id = session.get('user_id')
    user = User.find_by_id(user_id)

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()

        if not name:
            flash('Name cannot be empty.', 'warning')
        else:
            User.update_profile(user_id, name, phone, address)
            session['user_name'] = name
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('customer.profile'))

    return render_template('customer/profile.html', user=user)

@customer_bp.route('/about')
def about():
    return render_template('customer/about.html')

@customer_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        flash('Thank you for contacting us! We will get back to you shortly.', 'success')
        return redirect(url_for('customer.contact'))
    return render_template('customer/contact.html')
