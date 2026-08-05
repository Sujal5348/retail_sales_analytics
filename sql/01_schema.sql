-- ============================================================
-- Retail Sales Analytics System - Database Schema DDL (MySQL)
-- Tables: 11 Normalized Tables
-- ============================================================

CREATE DATABASE IF NOT EXISTS retail_sales_db;
USE retail_sales_db;

-- 1. Categories Table
DROP TABLE IF EXISTS OrderDetails;
DROP TABLE IF EXISTS Returns;
DROP TABLE IF EXISTS Payments;
DROP TABLE IF EXISTS Inventory;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Employees;
DROP TABLE IF EXISTS Stores;
DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Suppliers;
DROP TABLE IF EXISTS Categories;
DROP TABLE IF EXISTS Customers;

CREATE TABLE Categories (
    CategoryID INT AUTO_INCREMENT PRIMARY KEY,
    CategoryName VARCHAR(100) NOT NULL UNIQUE,
    Department VARCHAR(100) NOT NULL,
    Description TEXT,
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 2. Suppliers Table
CREATE TABLE Suppliers (
    SupplierID INT AUTO_INCREMENT PRIMARY KEY,
    SupplierName VARCHAR(150) NOT NULL,
    ContactName VARCHAR(100),
    Email VARCHAR(120) UNIQUE,
    Phone VARCHAR(30),
    City VARCHAR(100),
    Country VARCHAR(100) DEFAULT 'USA',
    Rating DECIMAL(3, 2) DEFAULT 4.00,
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 3. Products Table
CREATE TABLE Products (
    ProductID INT AUTO_INCREMENT PRIMARY KEY,
    SKU VARCHAR(50) NOT NULL UNIQUE,
    ProductName VARCHAR(200) NOT NULL,
    CategoryID INT NOT NULL,
    SupplierID INT NOT NULL,
    CostPrice DECIMAL(10, 2) NOT NULL CHECK (CostPrice >= 0),
    SellingPrice DECIMAL(10, 2) NOT NULL CHECK (SellingPrice >= 0),
    Status VARCHAR(20) DEFAULT 'Active' CHECK (Status IN ('Active', 'Discontinued', 'Out of Stock')),
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID) ON DELETE RESTRICT,
    FOREIGN KEY (SupplierID) REFERENCES Suppliers(SupplierID) ON DELETE RESTRICT
) ENGINE=InnoDB;

-- 4. Customers Table
CREATE TABLE Customers (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Email VARCHAR(120) NOT NULL UNIQUE,
    Phone VARCHAR(30),
    Gender VARCHAR(15) CHECK (Gender IN ('Male', 'Female', 'Non-binary', 'Other')),
    Age INT CHECK (Age BETWEEN 15 AND 100),
    City VARCHAR(100) NOT NULL,
    Region VARCHAR(50) NOT NULL,
    Segment VARCHAR(30) DEFAULT 'Regular' CHECK (Segment IN ('VIP', 'Regular', 'Occasional', 'New', 'At Risk')),
    JoinDate DATE NOT NULL,
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 5. Stores Table
CREATE TABLE Stores (
    StoreID INT AUTO_INCREMENT PRIMARY KEY,
    StoreName VARCHAR(100) NOT NULL UNIQUE,
    Location VARCHAR(200) NOT NULL,
    City VARCHAR(100) NOT NULL,
    Region VARCHAR(50) NOT NULL,
    StoreType VARCHAR(30) DEFAULT 'Flagship' CHECK (StoreType IN ('Flagship', 'Standard', 'Outlet', 'Express')),
    ManagerName VARCHAR(100),
    SquareFeet INT,
    OpenedDate DATE,
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 6. Employees Table
CREATE TABLE Employees (
    EmployeeID INT AUTO_INCREMENT PRIMARY KEY,
    StoreID INT NOT NULL,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Email VARCHAR(120) NOT NULL UNIQUE,
    Position VARCHAR(50) NOT NULL,
    MonthlyTarget DECIMAL(12, 2) DEFAULT 50000.00,
    HireDate DATE NOT NULL,
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (StoreID) REFERENCES Stores(StoreID) ON DELETE RESTRICT
) ENGINE=InnoDB;

-- 7. Orders Table
CREATE TABLE Orders (
    OrderID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT NOT NULL,
    StoreID INT NOT NULL,
    EmployeeID INT NOT NULL,
    OrderDate DATETIME NOT NULL,
    PaymentMethod VARCHAR(30) NOT NULL CHECK (PaymentMethod IN ('Credit Card', 'Debit Card', 'Cash', 'UPI', 'PayPal', 'Gift Card')),
    Status VARCHAR(20) DEFAULT 'Completed' CHECK (Status IN ('Completed', 'Pending', 'Cancelled', 'Returned')),
    TotalAmount DECIMAL(12, 2) DEFAULT 0.00,
    DiscountAmount DECIMAL(12, 2) DEFAULT 0.00,
    TaxAmount DECIMAL(12, 2) DEFAULT 0.00,
    CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID) ON DELETE RESTRICT,
    FOREIGN KEY (StoreID) REFERENCES Stores(StoreID) ON DELETE RESTRICT,
    FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID) ON DELETE RESTRICT
) ENGINE=InnoDB;

-- 8. OrderDetails Table
CREATE TABLE OrderDetails (
    OrderDetailID INT AUTO_INCREMENT PRIMARY KEY,
    OrderID INT NOT NULL,
    ProductID INT NOT NULL,
    Quantity INT NOT NULL CHECK (Quantity > 0),
    UnitPrice DECIMAL(10, 2) NOT NULL CHECK (UnitPrice >= 0),
    CostPrice DECIMAL(10, 2) NOT NULL CHECK (CostPrice >= 0),
    Discount DECIMAL(5, 2) DEFAULT 0.00 CHECK (Discount BETWEEN 0 AND 100),
    Tax DECIMAL(5, 2) DEFAULT 5.00 CHECK (Tax >= 0),
    LineTotal DECIMAL(12, 2) GENERATED ALWAYS AS (Quantity * UnitPrice * (1 - Discount/100) * (1 + Tax/100)) STORED,
    LineProfit DECIMAL(12, 2) GENERATED ALWAYS AS ((Quantity * UnitPrice * (1 - Discount/100)) - (Quantity * CostPrice)) STORED,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID) ON DELETE CASCADE,
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID) ON DELETE RESTRICT
) ENGINE=InnoDB;

-- 9. Inventory Table
CREATE TABLE Inventory (
    InventoryID INT AUTO_INCREMENT PRIMARY KEY,
    StoreID INT NOT NULL,
    ProductID INT NOT NULL,
    StockQuantity INT NOT NULL DEFAULT 0 CHECK (StockQuantity >= 0),
    ReorderLevel INT NOT NULL DEFAULT 20,
    LastRestockDate DATETIME,
    UpdatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY idx_store_product (StoreID, ProductID),
    FOREIGN KEY (StoreID) REFERENCES Stores(StoreID) ON DELETE CASCADE,
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 10. Payments Table
CREATE TABLE Payments (
    PaymentID INT AUTO_INCREMENT PRIMARY KEY,
    OrderID INT NOT NULL,
    PaymentDate DATETIME NOT NULL,
    Amount DECIMAL(12, 2) NOT NULL,
    PaymentMethod VARCHAR(30) NOT NULL,
    TransactionStatus VARCHAR(20) DEFAULT 'Success' CHECK (TransactionStatus IN ('Success', 'Failed', 'Refunded')),
    TransactionReference VARCHAR(100) UNIQUE,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 11. Returns Table
CREATE TABLE Returns (
    ReturnID INT AUTO_INCREMENT PRIMARY KEY,
    OrderID INT NOT NULL,
    ProductID INT NOT NULL,
    ReturnDate DATETIME NOT NULL,
    Quantity INT NOT NULL CHECK (Quantity > 0),
    Reason VARCHAR(150) NOT NULL,
    RefundAmount DECIMAL(12, 2) NOT NULL,
    Status VARCHAR(20) DEFAULT 'Approved' CHECK (Status IN ('Pending', 'Approved', 'Rejected')),
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID) ON DELETE CASCADE,
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID) ON DELETE RESTRICT
) ENGINE=InnoDB;

-- Indexes for Optimization
CREATE INDEX idx_orders_customer ON Orders(CustomerID);
CREATE INDEX idx_orders_store ON Orders(StoreID);
CREATE INDEX idx_orders_date ON Orders(OrderDate);
CREATE INDEX idx_orderdetails_order ON OrderDetails(OrderID);
CREATE INDEX idx_orderdetails_product ON OrderDetails(ProductID);
CREATE INDEX idx_products_category ON Products(CategoryID);
CREATE INDEX idx_products_supplier ON Products(SupplierID);
CREATE INDEX idx_customers_region ON Customers(Region);
