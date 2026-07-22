-- ============================================================
-- Retail Sales Analytics System - Database Views
-- ============================================================
USE retail_sales_db;

-- View 1: Executive KPI Overview
CREATE OR REPLACE VIEW vw_ExecutiveKPIs AS
SELECT 
    COUNT(DISTINCT o.OrderID) AS TotalOrders,
    COUNT(DISTINCT o.CustomerID) AS TotalActiveCustomers,
    COALESCE(SUM(od.Quantity * od.UnitPrice * (1 - od.Discount/100) * (1 + od.Tax/100)), 0) AS TotalRevenue,
    COALESCE(SUM((od.Quantity * od.UnitPrice * (1 - od.Discount/100)) - (od.Quantity * od.CostPrice)), 0) AS TotalProfit,
    ROUND(
        COALESCE(SUM((od.Quantity * od.UnitPrice * (1 - od.Discount/100)) - (od.Quantity * od.CostPrice)), 0) / 
        NULLIF(SUM(od.Quantity * od.UnitPrice * (1 - od.Discount/100)), 0) * 100, 2
    ) AS GrossMarginPercent,
    ROUND(COALESCE(SUM(od.Quantity * od.UnitPrice * (1 - od.Discount/100) * (1 + od.Tax/100)), 0) / NULLIF(COUNT(DISTINCT o.OrderID), 0), 2) AS AverageOrderValue
FROM Orders o
JOIN OrderDetails od ON o.OrderID = od.OrderID
WHERE o.Status != 'Cancelled';

-- View 2: Product Performance View
CREATE OR REPLACE VIEW vw_ProductPerformance AS
SELECT 
    p.ProductID,
    p.SKU,
    p.ProductName,
    c.CategoryName,
    c.Department,
    s.SupplierName,
    p.CostPrice,
    p.SellingPrice,
    COALESCE(SUM(od.Quantity), 0) AS UnitsSold,
    COALESCE(SUM(od.Quantity * od.UnitPrice * (1 - od.Discount/100)), 0) AS TotalRevenue,
    COALESCE(SUM((od.Quantity * od.UnitPrice * (1 - od.Discount/100)) - (od.Quantity * od.CostPrice)), 0) AS TotalProfit,
    ROUND(
        COALESCE(SUM((od.Quantity * od.UnitPrice * (1 - od.Discount/100)) - (od.Quantity * od.CostPrice)), 0) /
        NULLIF(SUM(od.Quantity * od.UnitPrice * (1 - od.Discount/100)), 0) * 100, 2
    ) AS ProfitMarginPercent
FROM Products p
JOIN Categories c ON p.CategoryID = c.CategoryID
JOIN Suppliers s ON p.SupplierID = s.SupplierID
LEFT JOIN OrderDetails od ON p.ProductID = od.ProductID
JOIN Orders o ON od.OrderID = o.OrderID AND o.Status != 'Cancelled'
GROUP BY p.ProductID, p.SKU, p.ProductName, c.CategoryName, c.Department, s.SupplierName, p.CostPrice, p.SellingPrice;

-- View 3: Customer Segment & Lifetime Value View
CREATE OR REPLACE VIEW vw_CustomerSegments AS
SELECT 
    c.CustomerID,
    CONCAT(c.FirstName, ' ', c.LastName) AS CustomerName,
    c.Email,
    c.City,
    c.Region,
    c.Segment,
    c.JoinDate,
    COUNT(DISTINCT o.OrderID) AS TotalOrders,
    COALESCE(SUM(od.Quantity * od.UnitPrice * (1 - od.Discount/100)), 0) AS LifetimeSpend,
    ROUND(COALESCE(SUM(od.Quantity * od.UnitPrice * (1 - od.Discount/100)), 0) / NULLIF(COUNT(DISTINCT o.OrderID), 0), 2) AS AverageOrderValue,
    MAX(o.OrderDate) AS LastOrderDate
FROM Customers c
LEFT JOIN Orders o ON c.CustomerID = o.CustomerID AND o.Status != 'Cancelled'
LEFT JOIN OrderDetails od ON o.OrderID = od.OrderID
GROUP BY c.CustomerID, c.FirstName, c.LastName, c.Email, c.City, c.Region, c.Segment, c.JoinDate;

-- View 4: Store & Regional Sales Performance
CREATE OR REPLACE VIEW vw_StoreRegionalPerformance AS
SELECT 
    st.StoreID,
    st.StoreName,
    st.City,
    st.Region,
    st.StoreType,
    st.ManagerName,
    COUNT(DISTINCT o.OrderID) AS TotalOrders,
    COALESCE(SUM(od.Quantity * od.UnitPrice * (1 - od.Discount/100)), 0) AS TotalRevenue,
    COALESCE(SUM((od.Quantity * od.UnitPrice * (1 - od.Discount/100)) - (od.Quantity * od.CostPrice)), 0) AS TotalProfit
FROM Stores st
LEFT JOIN Orders o ON st.StoreID = o.StoreID AND o.Status != 'Cancelled'
LEFT JOIN OrderDetails od ON o.OrderID = od.OrderID
GROUP BY st.StoreID, st.StoreName, st.City, st.Region, st.StoreType, st.ManagerName;

-- View 5: Inventory Valuation & Stock Alerts
CREATE OR REPLACE VIEW vw_InventoryStatus AS
SELECT 
    i.InventoryID,
    st.StoreName,
    st.Region,
    p.ProductID,
    p.SKU,
    p.ProductName,
    c.CategoryName,
    i.StockQuantity,
    i.ReorderLevel,
    p.CostPrice,
    p.SellingPrice,
    (i.StockQuantity * p.CostPrice) AS InventoryValuationAtCost,
    (i.StockQuantity * p.SellingPrice) AS InventoryValuationAtRetail,
    CASE 
        WHEN i.StockQuantity = 0 THEN 'Out of Stock'
        WHEN i.StockQuantity <= i.ReorderLevel THEN 'Low Stock'
        ELSE 'In Stock'
    END AS StockStatus
FROM Inventory i
JOIN Stores st ON i.StoreID = st.StoreID
JOIN Products p ON i.ProductID = p.ProductID
JOIN Categories c ON p.CategoryID = c.CategoryID;
