import pandas as pd
import numpy as np
from sqlalchemy import text
from models import db

def get_monthly_sales_trend():
    date_fmt = "STRFTIME('%Y-%m', o.OrderDate)" if db.engine.name == 'sqlite' else "DATE_FORMAT(o.OrderDate, '%Y-%m')"
    sql = text(f"""
    SELECT 
        {date_fmt} AS YearMonth,
        COUNT(DISTINCT o.OrderID) AS TotalOrders,
        SUM(od.Quantity * od.UnitPrice * (1 - od.Discount/100)) AS Revenue,
        SUM((od.Quantity * od.UnitPrice * (1 - od.Discount/100)) - (od.Quantity * od.CostPrice)) AS Profit
    FROM Orders o
    JOIN OrderDetails od ON o.OrderID = od.OrderID
    WHERE o.Status != 'Cancelled'
    GROUP BY {date_fmt}
    ORDER BY YearMonth ASC;
    """)
    df = pd.read_sql(sql, db.engine)
    if not df.empty:
        df['MoM_Growth'] = df['Revenue'].pct_change() * 100
        df['MoM_Growth'] = df['MoM_Growth'].fillna(0.0).round(2)
    return df

def get_category_performance():
    sql = text("""
    SELECT 
        c.CategoryName,
        c.Department,
        SUM(od.Quantity) AS UnitsSold,
        SUM(od.Quantity * od.UnitPrice * (1 - od.Discount/100)) AS TotalRevenue,
        SUM((od.Quantity * od.UnitPrice * (1 - od.Discount/100)) - (od.Quantity * od.CostPrice)) AS TotalProfit
    FROM Categories c
    JOIN Products p ON c.CategoryID = p.CategoryID
    JOIN OrderDetails od ON p.ProductID = od.ProductID
    JOIN Orders o ON od.OrderID = o.OrderID AND o.Status != 'Cancelled'
    GROUP BY c.CategoryName, c.Department
    ORDER BY TotalRevenue DESC;
    """)
    return pd.read_sql(sql, db.engine)

def get_regional_sales():
    sql = text("""
    SELECT 
        st.Region,
        COUNT(DISTINCT st.StoreID) AS TotalStores,
        COUNT(DISTINCT o.OrderID) AS TotalOrders,
        SUM(od.Quantity * od.UnitPrice * (1 - od.Discount/100)) AS Revenue,
        SUM((od.Quantity * od.UnitPrice * (1 - od.Discount/100)) - (od.Quantity * od.CostPrice)) AS Profit
    FROM Stores st
    LEFT JOIN Orders o ON st.StoreID = o.StoreID AND o.Status != 'Cancelled'
    LEFT JOIN OrderDetails od ON o.OrderID = od.OrderID
    GROUP BY st.Region
    ORDER BY Revenue DESC;
    """)
    return pd.read_sql(sql, db.engine)

def get_payment_method_distribution():
    sql = text("""
    SELECT 
        PaymentMethod,
        COUNT(OrderID) AS TransactionCount,
        SUM(TotalAmount) AS TotalVolume
    FROM Orders
    WHERE Status != 'Cancelled'
    GROUP BY PaymentMethod
    ORDER BY TotalVolume DESC;
    """)
    return pd.read_sql(sql, db.engine)

def get_top_products(limit=10):
    sql = text(f"""
    SELECT 
        p.ProductID,
        p.SKU,
        p.ProductName,
        c.CategoryName,
        SUM(od.Quantity) AS TotalUnitsSold,
        SUM(od.Quantity * od.UnitPrice * (1 - od.Discount/100)) AS TotalRevenue,
        SUM((od.Quantity * od.UnitPrice * (1 - od.Discount/100)) - (od.Quantity * od.CostPrice)) AS TotalProfit
    FROM Products p
    JOIN Categories c ON p.CategoryID = c.CategoryID
    JOIN OrderDetails od ON p.ProductID = od.ProductID
    JOIN Orders o ON od.OrderID = o.OrderID AND o.Status != 'Cancelled'
    GROUP BY p.ProductID, p.SKU, p.ProductName, c.CategoryName
    ORDER BY TotalRevenue DESC
    LIMIT {limit};
    """)
    return pd.read_sql(sql, db.engine)
