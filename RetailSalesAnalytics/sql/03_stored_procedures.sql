-- ============================================================
-- Retail Sales Analytics System - Stored Procedures
-- ============================================================
USE retail_sales_db;

DELIMITER //

-- Procedure 1: Get Low Stock Alert Report for a Store
DROP PROCEDURE IF EXISTS sp_LowStockAlerts //
CREATE PROCEDURE sp_LowStockAlerts(IN p_StoreID INT)
BEGIN
    SELECT 
        st.StoreName,
        p.SKU,
        p.ProductName,
        c.CategoryName,
        i.StockQuantity,
        i.ReorderLevel,
        (i.ReorderLevel - i.StockQuantity + 10) AS RecommendedReorderQty,
        s.SupplierName,
        s.Email AS SupplierContact
    FROM Inventory i
    JOIN Stores st ON i.StoreID = st.StoreID
    JOIN Products p ON i.ProductID = p.ProductID
    JOIN Categories c ON p.CategoryID = c.CategoryID
    JOIN Suppliers s ON p.SupplierID = s.SupplierID
    WHERE (p_StoreID IS NULL OR i.StoreID = p_StoreID)
      AND i.StockQuantity <= i.ReorderLevel
    ORDER BY i.StockQuantity ASC;
END //

-- Procedure 2: Calculate Customer Lifetime Value and Assign Segment
DROP PROCEDURE IF EXISTS sp_UpdateCustomerSegments //
CREATE PROCEDURE sp_UpdateCustomerSegments()
BEGIN
    UPDATE Customers c
    JOIN (
        SELECT 
            CustomerID,
            SUM(od.Quantity * od.UnitPrice * (1 - od.Discount/100)) AS TotalSpend,
            COUNT(DISTINCT o.OrderID) AS OrderCount
        FROM Orders o
        JOIN OrderDetails od ON o.OrderID = od.OrderID
        WHERE o.Status != 'Cancelled'
        GROUP BY CustomerID
    ) stats ON c.CustomerID = stats.CustomerID
    SET c.Segment = CASE
        WHEN stats.TotalSpend >= 5000 AND stats.OrderCount >= 5 THEN 'VIP'
        WHEN stats.TotalSpend >= 1500 THEN 'Regular'
        WHEN stats.TotalSpend > 0 THEN 'Occasional'
        ELSE 'New'
    END;
END //

-- Procedure 3: Monthly Store Sales & Target Achievement Report
DROP PROCEDURE IF EXISTS sp_StoreMonthlyPerformance //
CREATE PROCEDURE sp_StoreMonthlyPerformance(IN p_Year INT, IN p_Month INT)
BEGIN
    SELECT 
        st.StoreID,
        st.StoreName,
        st.Region,
        COUNT(DISTINCT o.OrderID) AS MonthlyOrders,
        COALESCE(SUM(od.Quantity * od.UnitPrice * (1 - od.Discount/100)), 0) AS ActualRevenue,
        COALESCE(SUM((od.Quantity * od.UnitPrice * (1 - od.Discount/100)) - (od.Quantity * od.CostPrice)), 0) AS ActualProfit,
        COUNT(DISTINCT e.EmployeeID) AS TotalStaff,
        COALESCE(SUM(e.MonthlyTarget), 0) AS CombinedStoreTarget,
        ROUND(
            (COALESCE(SUM(od.Quantity * od.UnitPrice * (1 - od.Discount/100)), 0) / 
            NULLIF(SUM(e.MonthlyTarget), 0)) * 100, 2
        ) AS TargetAchievementPercent
    FROM Stores st
    LEFT JOIN Employees e ON st.StoreID = e.StoreID
    LEFT JOIN Orders o ON st.StoreID = o.StoreID 
        AND YEAR(o.OrderDate) = p_Year 
        AND MONTH(o.OrderDate) = p_Month 
        AND o.Status != 'Cancelled'
    LEFT JOIN OrderDetails od ON o.OrderID = od.OrderID
    GROUP BY st.StoreID, st.StoreName, st.Region;
END //

DELIMITER ;
