from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.food import Food
from models.category import Category
from models.review import Review
from services.auth_service import login_required
from services.recommendation_service import RecommendationService

food_bp = Blueprint('food', __name__)

@food_bp.route('/menu')
def menu():
    search_query = request.args.get('search', '').strip()
    category_id = request.args.get('category', '').strip()
    price_range = request.args.get('price', '').strip()
    diet_type = request.args.get('diet', '').strip()

    foods = Food.get_all(
        search_query=search_query,
        category_id=category_id,
        price_range=price_range,
        diet_type=diet_type
    )

    categories = Category.get_all()

    return render_template('customer/menu.html',
                           foods=foods,
                           categories=categories,
                           selected_category=category_id,
                           selected_price=price_range,
                           selected_diet=diet_type,
                           search_query=search_query)

@food_bp.route('/food/<int:food_id>')
def food_details(food_id):
    food = Food.get_by_id(food_id)
    if not food:
        flash('Food item not found.', 'danger')
        return redirect(url_for('food.menu'))

    reviews = Review.get_by_food(food_id)
    similar_recs = RecommendationService.get_recommendations_for_food(food_id, top_n=4)

    return render_template('customer/food_details.html',
                           food=food,
                           reviews=reviews,
                           similar_recs=similar_recs)

@food_bp.route('/food/<int:food_id>/review', methods=['POST'])
@login_required
def add_review(food_id):
    user_id = session.get('user_id')
    rating = int(request.form.get('rating', 5))
    comment = request.form.get('comment', '').strip()

    Review.create(user_id, food_id, rating, comment)
    flash('Thank you for your rating & review!', 'success')
    return redirect(url_for('food.food_details', food_id=food_id))

@food_bp.route('/search')
def search():
    query = request.args.get('q', '').strip()
    foods = Food.get_all(search_query=query)
    categories = Category.get_all()
    return render_template('customer/menu.html',
                           foods=foods,
                           categories=categories,
                           search_query=query)
