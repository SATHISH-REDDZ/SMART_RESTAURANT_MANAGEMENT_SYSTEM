from analytics.sales_analysis import SalesAnalysis
from analytics.order_analysis import OrderAnalysis

class AnalyticsReport:
    @classmethod
    def generate_full_admin_report(cls):
        metrics = SalesAnalysis.get_summary_metrics()
        sales_by_day = SalesAnalysis.get_sales_by_day()
        sales_by_category = SalesAnalysis.get_sales_by_category()
        top_foods = SalesAnalysis.get_top_foods()
        status_breakdown = OrderAnalysis.get_status_breakdown()
        payment_methods = OrderAnalysis.get_payment_method_breakdown()

        return {
            'metrics': metrics,
            'sales_by_day': sales_by_day,
            'sales_by_category': sales_by_category,
            'top_foods': top_foods,
            'status_breakdown': status_breakdown,
            'payment_methods': payment_methods
        }
