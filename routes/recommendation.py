from flask import Blueprint, render_template, session
from services.recommendation_service import RecommendationService

recommendation_bp = Blueprint('recommendation', __name__)

@recommendation_bp.route('/recommendations')
def view_recommendations():
    user_id = session.get('user_id')
    if user_id:
        personalized = RecommendationService.get_recommendations_for_user(user_id, top_n=6)
    else:
        personalized = RecommendationService.get_popular_recommendations(top_n=6)

    popular = RecommendationService.get_popular_recommendations(top_n=6)

    return render_template('customer/recommendations.html',
                           personalized=personalized,
                           popular=popular)
