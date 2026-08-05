from .main import main_bp
from .sales import sales_bp
from .customers import customers_bp
from .inventory import inventory_bp
from .stores import stores_bp
from .employees import employees_bp
from .analytics_api import analytics_bp

def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(sales_bp, url_prefix='/sales')
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    app.register_blueprint(stores_bp, url_prefix='/stores')
    app.register_blueprint(employees_bp, url_prefix='/employees')
    app.register_blueprint(analytics_bp, url_prefix='/analytics')
