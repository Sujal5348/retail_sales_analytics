-- ============================================================
-- Retail Sales Analytics System - Advanced Analytics Queries
-- Demonstrates: INNER/LEFT/RIGHT JOIN, GROUP BY, HAVING, ORDER BY,
-- Aggregate Functions, CASE, Subqueries, CTEs, Window Functions
-- ============================================================
USE retail_sales_db;

-- ------------------------------------------------------------
-- Q1: Top 10 Selling Products by Revenue (Window Functions & CTE)
-- ------------------------------------------------------------
WITH ProductRevenueCTE AS (
    SELECT 
        p.ProductID,
        p.ProductName,
        c.CategoryName,
        SUM(od.Quantity) AS TotalUnitsSold,
        SUM(od.Quantity * od.UnitPrice * (1 - od.Discount/100)) AS TotalRevenue,
        SUM((od.Quantity * od.UnitPrice * (1 - od.Discount/100)) - (od.Quantity * od.CostPrice)) AS TotalProfit,
        DENSE_RANK() OVER (ORDER BY SUM(od.Quantity * od.UnitPrice * (1 - od.Discount/100)) DESC) AS RevenueRank
    FROM Products p
    JOIN Categories c ON p.CategoryID = c.CategoryID
    JOIN OrderDetails od ON p.ProductID = od.ProductID
    JOIN Orders o ON od.OrderID = o.OrderID AND o.Status != 'Cancelled'
    GROUP BY p.ProductID, p.ProductName, c.CategoryName
)
SELECT * FROM ProductRevenueCTE
WHERE RevenueRank <= 10;


-- ------------------------------------------------------------
-- Q2: Monthly Sales Trends & Month-over-Month (MoM) Growth Rate (LAG Window Function)
-- ------------------------------------------------------------
WITH MonthlySalesCTE AS (
    SELECT 
        DATE_FORMAT(o.OrderDate, '%Y-%m') AS YearMonth,
        COUNT(DISTINCT o.OrderID) AS TotalOrders,
        SUM(od.Quantity * od.UnitPrice * (1 - od.Discount/100)) AS MonthlyRevenue,
        SUM((od.Quantity * od.UnitPrice * (1 - od.Discount/100)) - (od.Quantity * od.CostPrice)) AS MonthlyProfit
    FROM Orders o
    JOIN OrderDetails od ON o.OrderID = od.OrderID
    WHERE o.Status != 'Cancelled'
    GROUP BY DATE_FORMAT(o.OrderDate, '%Y-%m')
)
SELECT 
    YearMonth,
    TotalOrders,
    ROUND(MonthlyRevenue, 2) AS MonthlyRevenue,
    ROUND(MonthlyProfit, 2) AS MonthlyProfit,
    ROUND(LAG(MonthlyRevenue, 1) OVER (ORDER BY YearMonth), 2) AS PrevMonthRevenue,
    ROUND(
        (MonthlyRevenue - LAG(MonthlyRevenue, 1) OVER (ORDER BY YearMonth)) / 
        NULLIF(LAG(MonthlyRevenue, 1) OVER (ORDER BY YearMonth), 0) * 100, 2
    ) AS MoM_Growth_Percent
FROM MonthlySalesCTE
ORDER BY YearMonth ASC;


-- ------------------------------------------------------------
-- Q3: Customer Segmentation & Lifetime Value Analysis (CASE + Subquery + GROUP BY + HAVING)
-- ------------------------------------------------------------
SELECT 
    CASE 
        WHEN TotalSpend >= 5000 THEN 'VIP Customer ($5,000+)'
        WHEN TotalSpend >= 2000 THEN 'High Value ($2,000-$4,999)'
        WHEN TotalSpend >= 500 THEN 'Mid Tier ($500-$1,999)'
        ELSE 'Low Tier (<$500)'
    END AS CustomerCategory,
    COUNT(CustomerID) AS TotalCustomers,
    ROUND(AVG(TotalSpend), 2) AS AvgCustomerSpend,
    ROUND(SUM(TotalSpend), 2) AS CombinedCategoryRevenue
FROM (
    SELECT 
        c.CustomerID,
        SUM(od.Quantity * od.UnitPrice * (1 - od.Discount/100)) AS TotalSpend
    FROM Customers c
    JOIN Orders o ON c.CustomerID = o.CustomerID AND o.Status != 'Cancelled'
    JOIN OrderDetails od ON o.OrderID = od.OrderID
    GROUP BY c.CustomerID
) CustomerSpendSummary
GROUP BY CustomerCategory
ORDER BY CombinedCategoryRevenue DESC;


-- ------------------------------------------------------------
-- Q4: Store Performance Leaderboard with Running Total Revenue (SUM OVER)
-- ------------------------------------------------------------
SELECT 
    st.StoreID,
    st.StoreName,
    st.Region,
    COUNT(DISTINCT o.OrderID) AS OrderCount,
    ROUND(SUM(od.Quantity * od.UnitPrice * (1 - od.Discount/100)), 2) AS StoreRevenue,
    ROUND(
        SUM(SUM(od.Quantity * od.UnitPrice * (1 - od.Discount/100))) OVER (PARTITION BY st.Region ORDER BY SUM(od.Quantity * od.UnitPrice * (1 - od.Discount/100)) DESC), 2
    ) AS RegionalRunningTotalRevenue
FROM Stores st
LEFT JOIN Orders o ON st.StoreID = o.StoreID AND o.Status != 'Cancelled'
LEFT JOIN OrderDetails od ON o.OrderID = od.OrderID
GROUP BY st.StoreID, st.StoreName, st.Region
ORDER BY st.Region, StoreRevenue DESC;


-- ------------------------------------------------------------
-- Q5: Employee Target Achievement & Performance Ranking (Window Function + LEFT JOIN)
-- ------------------------------------------------------------
SELECT 
    e.EmployeeID,
    CONCAT(e.FirstName, ' ', e.LastName) AS EmployeeName,
    st.StoreName,
    e.MonthlyTarget,
    ROUND(COALESCE(SUM(od.Quantity * od.UnitPrice * (1 - od.Discount/100)), 0), 2) AS TotalSalesAchieved,
    ROUND(
        (COALESCE(SUM(od.Quantity * od.UnitPrice * (1 - od.Discount/100)), 0) / NULLIF(e.MonthlyTarget, 0)) * 100, 2
    ) AS TargetAchievementPercent,
    RANK() OVER (ORDER BY COALESCE(SUM(od.Quantity * od.UnitPrice * (1 - od.Discount/100)), 0) DESC) AS OverallEmployeeRank
FROM Employees e
JOIN Stores st ON e.StoreID = st.StoreID
LEFT JOIN Orders o ON e.EmployeeID = o.EmployeeID AND o.Status != 'Cancelled'
LEFT JOIN OrderDetails od ON o.OrderID = od.OrderID
GROUP BY e.EmployeeID, e.FirstName, e.LastName, st.StoreName, e.MonthlyTarget
HAVING TotalSalesAchieved > 0
ORDER BY TotalSalesAchieved DESC;


-- ------------------------------------------------------------
-- Q6: Low Stock & Reorder Valuation Alert Report (Subquery + JOIN)
-- ------------------------------------------------------------
SELECT 
    st.StoreName,
    p.SKU,
    p.ProductName,
    c.CategoryName,
    i.StockQuantity,
    i.ReorderLevel,
    p.CostPrice,
    ROUND((i.ReorderLevel - i.StockQuantity + 20) * p.CostPrice, 2) AS EstimatedRestockCost
FROM Inventory i
JOIN Stores st ON i.StoreID = st.StoreID
JOIN Products p ON i.ProductID = p.ProductID
JOIN Categories c ON p.CategoryID = c.CategoryID
WHERE i.StockQuantity <= i.ReorderLevel
ORDER BY (i.ReorderLevel - i.StockQuantity) DESC;


-- ------------------------------------------------------------
-- Q7: Product Return Rate & Refund Impact Analysis
-- ------------------------------------------------------------
SELECT 
    p.ProductID,
    p.ProductName,
    c.CategoryName,
    COALESCE(SUM(od.Quantity), 0) AS TotalSoldQuantity,
    COALESCE(SUM(r.Quantity), 0) AS TotalReturnedQuantity,
    ROUND((COALESCE(SUM(r.Quantity), 0) / NULLIF(SUM(od.Quantity), 0)) * 100, 2) AS ReturnRatePercent,
    COALESCE(SUM(r.RefundAmount), 0) AS TotalRefundAmount
FROM Products p
JOIN Categories c ON p.CategoryID = c.CategoryID
LEFT JOIN OrderDetails od ON p.ProductID = od.ProductID
LEFT JOIN Returns r ON od.OrderID = r.OrderID AND od.ProductID = r.ProductID
GROUP BY p.ProductID, p.ProductName, c.CategoryName
HAVING TotalReturnedQuantity > 0
ORDER BY ReturnRatePercent DESC;


-- ------------------------------------------------------------
-- Q8: Customer Retention Rate & Repeat vs New Customer Analysis
-- ------------------------------------------------------------
WITH CustomerOrderCounts AS (
    SELECT 
        CustomerID,
        COUNT(OrderID) AS OrderCount
    FROM Orders
    WHERE Status != 'Cancelled'
    GROUP BY CustomerID
)
SELECT 
    COUNT(CustomerID) AS TotalActiveCustomers,
    SUM(CASE WHEN OrderCount = 1 THEN 1 ELSE 0 END) AS OneTimeCustomers,
    SUM(CASE WHEN OrderCount > 1 THEN 1 ELSE 0 END) AS RepeatCustomers,
    ROUND((SUM(CASE WHEN OrderCount > 1 THEN 1 ELSE 0 END) / COUNT(CustomerID)) * 100, 2) AS CustomerRetentionRatePercent
FROM CustomerOrderCounts;
