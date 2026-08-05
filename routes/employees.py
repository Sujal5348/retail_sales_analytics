from flask import Blueprint, render_template
from sqlalchemy import text
from models import db

employees_bp = Blueprint('employees', __name__)

@employees_bp.route('/')
def employee_performance():
    concat_name = "(e.FirstName || ' ' || e.LastName)" if db.engine.name == 'sqlite' else "CONCAT(e.FirstName, ' ', e.LastName)"
    sql = text(f"""
    SELECT 
        e.EmployeeID,
        {concat_name} AS EmployeeName,
        st.StoreName,
        st.Region,
        e.Position,
        e.MonthlyTarget,
        COALESCE(SUM(od.Quantity * od.UnitPrice * (1 - od.Discount/100)), 0) AS TotalSales,
        ROUND((COALESCE(SUM(od.Quantity * od.UnitPrice * (1 - od.Discount/100)), 0) / NULLIF(e.MonthlyTarget, 0)) * 100, 2) AS TargetAchievementPct
    FROM Employees e
    JOIN Stores st ON e.StoreID = st.StoreID
    LEFT JOIN Orders o ON e.EmployeeID = o.EmployeeID AND o.Status != 'Cancelled'
    LEFT JOIN OrderDetails od ON o.OrderID = od.OrderID
    GROUP BY e.EmployeeID, e.FirstName, e.LastName, st.StoreName, st.Region, e.Position, e.MonthlyTarget
    ORDER BY TotalSales DESC;
    """)
    employees = db.session.execute(sql).fetchall()
    return render_template('employees.html', employees=employees)
