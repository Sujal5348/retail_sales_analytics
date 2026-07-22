import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import create_app
from models import db, Order, OrderDetail, Customer, Product, Store, Inventory
from analytics.kpi_calculator import calculate_executive_kpis
from reports.report_generator import generate_excel_report

print("--- Starting System Integration & Verification Tests ---")

app = create_app()

with app.app_context():
    print("\n1. Testing Database Row Counts...")
    print(f"Products Count: {Product.query.count():,}")
    print(f"Customers Count: {Customer.query.count():,}")
    print(f"Orders Count: {Order.query.count():,}")
    print(f"OrderDetails Count: {OrderDetail.query.count():,}")
    print(f"Inventory Items Count: {Inventory.query.count():,}")

    assert Product.query.count() >= 2000, "Products count check failed!"
    assert Customer.query.count() >= 10000, "Customers count check failed!"
    assert OrderDetail.query.count() >= 100000, "OrderDetails count check failed!"
    print("[PASS] Database table row counts verified!")

    print("\n2. Testing KPI Calculator Math Engine...")
    kpis = calculate_executive_kpis()
    print(f"Total Revenue: ${kpis['total_revenue']:,.2f}")
    print(f"Total Net Profit: ${kpis['total_profit']:,.2f}")
    print(f"Gross Margin %: {kpis['gross_margin_pct']}%")
    print(f"Average Order Value: ${kpis['aov']:,.2f}")
    print(f"Stock Turnover Ratio: {kpis['stock_turnover']}x")
    print(f"Product Return Rate: {kpis['return_rate_pct']}%")
    
    assert kpis['total_revenue'] > 0, "Revenue should be greater than 0"
    assert kpis['gross_margin_pct'] > 0, "Gross margin should be positive"
    print("[PASS] Executive KPI calculation verified!")

    print("\n3. Testing Automated Excel Report Exporter...")
    filepath = generate_excel_report()
    assert os.path.exists(filepath), "Excel report file was not generated!"
    print(f"[PASS] Excel report generated at {filepath}")

    print("\n4. Testing Flask Endpoint Routes...")
    client = app.test_client()

    routes_to_test = [
        '/',
        '/sales',
        '/customers',
        '/inventory',
        '/stores',
        '/employees',
        '/analytics',
        '/api/dashboard-charts'
    ]

    for route in routes_to_test:
        response = client.get(route)
        assert response.status_code == 200, f"Route {route} failed with status {response.status_code}"
        print(f"[PASS] GET {route} -> HTTP 200 OK")

print("\n=== ALL SYSTEM INTEGRATION & VERIFICATION TESTS PASSED SUCCESSFULLY! ===")
