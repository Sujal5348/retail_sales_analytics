-- ============================================================
-- Retail Sales Analytics System - Triggers
-- ============================================================
USE retail_sales_db;

DELIMITER //

-- Trigger 1: Automatically Deduct Inventory Stock when Order Details are Created
DROP TRIGGER IF EXISTS trg_AfterOrderDetailsInsert //
CREATE TRIGGER trg_AfterOrderDetailsInsert
AFTER INSERT ON OrderDetails
FOR EACH ROW
BEGIN
    DECLARE v_StoreID INT;
    
    -- Get StoreID for the associated order
    SELECT StoreID INTO v_StoreID 
    FROM Orders 
    WHERE OrderID = NEW.OrderID;
    
    -- Deduct inventory
    UPDATE Inventory
    SET StockQuantity = GREATEST(0, StockQuantity - NEW.Quantity)
    WHERE StoreID = v_StoreID AND ProductID = NEW.ProductID;
END //

-- Trigger 2: Restore Inventory Stock when a Product Return is Approved
DROP TRIGGER IF EXISTS trg_AfterReturnInsert //
CREATE TRIGGER trg_AfterReturnInsert
AFTER INSERT ON Returns
FOR EACH ROW
BEGIN
    DECLARE v_StoreID INT;
    
    IF NEW.Status = 'Approved' THEN
        SELECT StoreID INTO v_StoreID 
        FROM Orders 
        WHERE OrderID = NEW.OrderID;
        
        UPDATE Inventory
        SET StockQuantity = StockQuantity + NEW.Quantity
        WHERE StoreID = v_StoreID AND ProductID = NEW.ProductID;
    END IF;
END //

DELIMITER ;
