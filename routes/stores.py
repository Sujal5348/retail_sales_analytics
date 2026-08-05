from flask import Blueprint, render_template, jsonify
from sqlalchemy import text
from models import db

stores_bp = Blueprint('stores', __name__)

@stores_bp.route('/')
def store_performance():
    sql = text("""
    SELECT 
        st.StoreID,
        st.StoreName,
        st.City,
        st.Region,
        st.StoreType,
        st.ManagerName,
        COUNT(DISTINCT o.OrderID) AS TotalOrders,
        COALESCE(SUM(od.Quantity * od.UnitPrice * (1 - od.Discount/100)), 0) AS Revenue,
        COALESCE(SUM((od.Quantity * od.UnitPrice * (1 - od.Discount/100)) - (od.Quantity * od.CostPrice)), 0) AS Profit
    FROM Stores st
    LEFT JOIN Orders o ON st.StoreID = o.StoreID AND o.Status != 'Cancelled'
    LEFT JOIN OrderDetails od ON o.OrderID = od.OrderID
    GROUP BY st.StoreID, st.StoreName, st.City, st.Region, st.StoreType, st.ManagerName
    ORDER BY Revenue DESC;
    """)
    stores_data = db.session.execute(sql).fetchall()
    return render_template('stores.html', stores=stores_data)
