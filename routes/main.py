from flask import Blueprint, render_template, jsonify
from analytics.kpi_calculator import calculate_executive_kpis
from analytics.eda_engine import (
    get_monthly_sales_trend, 
    get_category_performance, 
    get_regional_sales, 
    get_payment_method_distribution,
    get_top_products
)

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def dashboard():
    kpis = calculate_executive_kpis()
    return render_template('dashboard.html', kpis=kpis)

@main_bp.route('/api/dashboard-charts')
def dashboard_charts_api():
    monthly_trend = get_monthly_sales_trend().to_dict(orient='records')
    category_perf = get_category_performance().to_dict(orient='records')
    regional_sales = get_regional_sales().to_dict(orient='records')
    payment_methods = get_payment_method_distribution().to_dict(orient='records')
    top_prods = get_top_products(10).to_dict(orient='records')

    return jsonify({
        'monthly_trend': monthly_trend,
        'category_perf': category_perf,
        'regional_sales': regional_sales,
        'payment_methods': payment_methods,
        'top_products': top_prods
    })
