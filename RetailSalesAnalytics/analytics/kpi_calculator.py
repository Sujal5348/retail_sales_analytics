import pandas as pd
import numpy as np
from sqlalchemy import text
from models import db

def calculate_executive_kpis():
    """
    Returns core retail business KPIs:
    - Total Sales / Orders
    - Total Revenue
    - Total Profit
    - Gross Margin %
    - Average Order Value (AOV)
    - Total Customers & Segment Breakdown
    - Stock Turnover & Inventory Value
    - Return Rate %
    """
    sql = text("""
    SELECT 
        COUNT(DISTINCT o.OrderID) AS total_orders,
        COUNT(DISTINCT o.CustomerID) AS active_customers,
        COALESCE(SUM(od.Quantity * od.UnitPrice * (1 - od.Discount/100) * (1 + od.Tax/100)), 0) AS total_revenue,
        COALESCE(SUM((od.Quantity * od.UnitPrice * (1 - od.Discount/100)) - (od.Quantity * od.CostPrice)), 0) AS total_profit,
        COALESCE(SUM(od.Quantity), 0) AS total_units_sold
    FROM Orders o
    JOIN OrderDetails od ON o.OrderID = od.OrderID
    WHERE o.Status != 'Cancelled';
    """)
    
    result = db.session.execute(sql).fetchone()
    
    total_orders = result.total_orders or 0
    active_customers = result.active_customers or 0
    total_revenue = float(result.total_revenue or 0.0)
    total_profit = float(result.total_profit or 0.0)
    total_units = result.total_units_sold or 0
    
    gross_margin_pct = round((total_profit / total_revenue * 100), 2) if total_revenue > 0 else 0.0
    aov = round((total_revenue / total_orders), 2) if total_orders > 0 else 0.0

    # Total Inventory Valuation
    inv_sql = text("""
    SELECT 
        COALESCE(SUM(i.StockQuantity * p.CostPrice), 0) AS total_inv_cost,
        COALESCE(SUM(i.StockQuantity * p.SellingPrice), 0) AS total_inv_retail,
        COALESCE(SUM(CASE WHEN i.StockQuantity <= i.ReorderLevel THEN 1 ELSE 0 END), 0) AS low_stock_count
    FROM Inventory i
    JOIN Products p ON i.ProductID = p.ProductID;
    """)
    inv_res = db.session.execute(inv_sql).fetchone()
    inv_valuation_cost = float(inv_res.total_inv_cost or 0.0)
    inv_valuation_retail = float(inv_res.total_inv_retail or 0.0)
    low_stock_count = inv_res.low_stock_count or 0

    # Stock Turnover Ratio = Cost of Goods Sold (COGS) / Average Inventory Cost
    cogs = total_revenue - total_profit
    stock_turnover = round((cogs / inv_valuation_cost), 2) if inv_valuation_cost > 0 else 0.0

    # Return Rate %
    ret_sql = text("""
    SELECT 
        COALESCE(SUM(r.Quantity), 0) AS returned_qty,
        COALESCE(SUM(r.RefundAmount), 0) AS total_refunds
    FROM Returns r;
    """)
    ret_res = db.session.execute(ret_sql).fetchone()
    returned_qty = ret_res.returned_qty or 0
    total_refunds = float(ret_res.total_refunds or 0.0)
    return_rate_pct = round((returned_qty / total_units * 100), 2) if total_units > 0 else 0.0

    # Customer Metrics (Total, New, Repeat)
    cust_sql = text("""
    SELECT 
        COUNT(CustomerID) AS total_cust,
        SUM(CASE WHEN order_count = 1 THEN 1 ELSE 0 END) AS new_cust,
        SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) AS repeat_cust
    FROM (
        SELECT CustomerID, COUNT(OrderID) AS order_count 
        FROM Orders WHERE Status != 'Cancelled' GROUP BY CustomerID
    );
    """)
    cust_res = db.session.execute(cust_sql).fetchone()
    total_cust = cust_res.total_cust or 0
    new_cust = cust_res.new_cust or 0
    repeat_cust = cust_res.repeat_cust or 0
    retention_rate = round((repeat_cust / total_cust * 100), 2) if total_cust > 0 else 0.0

    return {
        'total_orders': total_orders,
        'active_customers': active_customers,
        'total_revenue': total_revenue,
        'total_profit': total_profit,
        'gross_margin_pct': gross_margin_pct,
        'aov': aov,
        'inv_valuation_cost': inv_valuation_cost,
        'inv_valuation_retail': inv_valuation_retail,
        'low_stock_count': low_stock_count,
        'stock_turnover': stock_turnover,
        'total_units_sold': total_units,
        'returned_qty': returned_qty,
        'total_refunds': total_refunds,
        'return_rate_pct': return_rate_pct,
        'total_cust': total_cust,
        'new_cust': new_cust,
        'repeat_cust': repeat_cust,
        'retention_rate': retention_rate
    }
