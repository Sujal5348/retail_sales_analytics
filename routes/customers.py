from flask import Blueprint, render_template, request, jsonify
from sqlalchemy import text
from models import db, Customer

customers_bp = Blueprint('customers', __name__)

@customers_bp.route('/')
def customer_list():
    segment_filter = request.args.get('segment', '')
    region_filter = request.args.get('region', '')
    page = request.args.get('page', 1, type=int)

    # Base query for top customers by spend
    concat_name = "(c.FirstName || ' ' || c.LastName)" if db.engine.name == 'sqlite' else "CONCAT(c.FirstName, ' ', c.LastName)"
    sql = f"""
    SELECT 
        c.CustomerID,
        {concat_name} AS CustomerName,
        c.Email,
        c.City,
        c.Region,
        c.Segment,
        c.JoinDate,
        COUNT(DISTINCT o.OrderID) AS OrderCount,
        COALESCE(SUM(od.Quantity * od.UnitPrice * (1 - od.Discount/100)), 0) AS TotalSpend
    FROM Customers c
    LEFT JOIN Orders o ON c.CustomerID = o.CustomerID AND o.Status != 'Cancelled'
    LEFT JOIN OrderDetails od ON o.OrderID = od.OrderID
    WHERE 1=1
    """
    params = {}
    if segment_filter:
        sql += " AND c.Segment = :segment"
        params['segment'] = segment_filter
    if region_filter:
        sql += " AND c.Region = :region"
        params['region'] = region_filter

    sql += " GROUP BY c.CustomerID, c.FirstName, c.LastName, c.Email, c.City, c.Region, c.Segment, c.JoinDate"
    sql += " ORDER BY TotalSpend DESC LIMIT 100"

    result = db.session.execute(text(sql), params).fetchall()

    segments = ['VIP', 'Regular', 'Occasional', 'New']
    regions = ['North', 'South', 'East', 'West', 'Midwest']

    return render_template('customers.html', 
                           customers=result, 
                           segments=segments, 
                           regions=regions,
                           current_segment=segment_filter,
                           current_region=region_filter)
