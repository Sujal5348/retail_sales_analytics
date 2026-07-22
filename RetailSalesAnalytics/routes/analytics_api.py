from flask import Blueprint, render_template, request, jsonify, send_file
from sqlalchemy import text
from models import db
from reports.report_generator import generate_excel_report

analytics_bp = Blueprint('analytics', __name__)

PREBUILT_QUERIES = {
    'q1_top_products': {
        'name': 'Top 10 Selling Products by Revenue',
        'sql': """
SELECT 
    p.ProductID, p.SKU, p.ProductName, c.CategoryName,
    SUM(od.Quantity) AS TotalUnitsSold,
    ROUND(SUM(od.Quantity * od.UnitPrice * (1 - od.Discount/100)), 2) AS TotalRevenue,
    ROUND(SUM((od.Quantity * od.UnitPrice * (1 - od.Discount/100)) - (od.Quantity * od.CostPrice)), 2) AS TotalProfit
FROM Products p
JOIN Categories c ON p.CategoryID = c.CategoryID
JOIN OrderDetails od ON p.ProductID = od.ProductID
JOIN Orders o ON od.OrderID = o.OrderID AND o.Status != 'Cancelled'
GROUP BY p.ProductID, p.SKU, p.ProductName, c.CategoryName
ORDER BY TotalRevenue DESC
LIMIT 10;
        """
    },
    'q2_mom_growth': {
        'name': 'Monthly Sales Trends & MoM Growth (Window Function)',
        'sql': """
WITH MonthlySales AS (
    SELECT 
        STRFTIME('%Y-%m', o.OrderDate) AS YearMonth,
        COUNT(DISTINCT o.OrderID) AS TotalOrders,
        SUM(od.Quantity * od.UnitPrice * (1 - od.Discount/100)) AS MonthlyRevenue
    FROM Orders o
    JOIN OrderDetails od ON o.OrderID = od.OrderID
    WHERE o.Status != 'Cancelled'
    GROUP BY STRFTIME('%Y-%m', o.OrderDate)
)
SELECT 
    YearMonth,
    TotalOrders,
    ROUND(MonthlyRevenue, 2) AS MonthlyRevenue,
    ROUND(LAG(MonthlyRevenue, 1) OVER (ORDER BY YearMonth), 2) AS PrevMonthRevenue,
    ROUND(((MonthlyRevenue - LAG(MonthlyRevenue, 1) OVER (ORDER BY YearMonth)) / LAG(MonthlyRevenue, 1) OVER (ORDER BY YearMonth)) * 100, 2) AS MoM_Growth_Pct
FROM MonthlySales
ORDER BY YearMonth ASC;
        """
    },
    'q3_customer_clv': {
        'name': 'Customer Lifetime Value & Spending Tiers',
        'sql': """
SELECT 
    c.CustomerID,
    c.FirstName || ' ' || c.LastName AS CustomerName,
    c.Region,
    c.Segment,
    COUNT(DISTINCT o.OrderID) AS OrderCount,
    ROUND(SUM(od.Quantity * od.UnitPrice * (1 - od.Discount/100)), 2) AS LifetimeSpend,
    CASE 
        WHEN SUM(od.Quantity * od.UnitPrice * (1 - od.Discount/100)) >= 5000 THEN 'VIP ($5,000+)'
        WHEN SUM(od.Quantity * od.UnitPrice * (1 - od.Discount/100)) >= 2000 THEN 'High Value'
        WHEN SUM(od.Quantity * od.UnitPrice * (1 - od.Discount/100)) >= 500 THEN 'Mid Tier'
        ELSE 'Low Tier'
    END AS Tier
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID AND o.Status != 'Cancelled'
JOIN OrderDetails od ON o.OrderID = od.OrderID
GROUP BY c.CustomerID, c.FirstName, c.LastName, c.Region, c.Segment
ORDER BY LifetimeSpend DESC
LIMIT 20;
        """
    },
    'q4_low_stock': {
        'name': 'Low Stock & Reorder Alert Report',
        'sql': """
SELECT 
    st.StoreName,
    p.SKU,
    p.ProductName,
    c.CategoryName,
    i.StockQuantity,
    i.ReorderLevel,
    (i.ReorderLevel - i.StockQuantity + 20) AS RecommendedReorder
FROM Inventory i
JOIN Stores st ON i.StoreID = st.StoreID
JOIN Products p ON i.ProductID = p.ProductID
JOIN Categories c ON p.CategoryID = c.CategoryID
WHERE i.StockQuantity <= i.ReorderLevel
ORDER BY i.StockQuantity ASC
LIMIT 30;
        """
    }
}

@analytics_bp.route('/')
def analytics_studio():
    return render_template('analytics.html', prebuilt=PREBUILT_QUERIES)

@analytics_bp.route('/execute', methods=['POST'])
def execute_sql():
    data = request.json or {}
    query_key = data.get('query_key')
    custom_sql = data.get('sql')
    
    if query_key in PREBUILT_QUERIES:
        sql_to_run = PREBUILT_QUERIES[query_key]['sql']
    elif custom_sql:
        sql_to_run = custom_sql
    else:
        return jsonify({'success': False, 'error': 'No query provided'}), 400

    try:
        res = db.session.execute(text(sql_to_run))
        columns = list(res.keys())
        rows = [list(row) for row in res.fetchall()]
        return jsonify({
            'success': True,
            'columns': columns,
            'rows': rows,
            'row_count': len(rows)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@analytics_bp.route('/reports')
def reports_page():
    return render_template('reports.html')

@analytics_bp.route('/export/excel')
def export_excel():
    filepath = generate_excel_report()
    return send_file(filepath, as_attachment=True, download_name='Retail_Sales_Executive_Report.xlsx')
