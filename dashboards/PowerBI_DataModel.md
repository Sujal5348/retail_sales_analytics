# Power BI Data Model Architecture & Schema Design

The **Retail Sales Analytics System** uses a **Star Schema** data model in Power BI designed for maximum analytical query performance.

## Relational Diagram

```
                 +-------------------+
                 |    Categories     |
                 +-------------------+
                           | 1
                           |
                           | *
                 +-------------------+
                 |     Products      |
                 +-------------------+
                 |  *           *    |
                 |              |    | 1
                 | 1            +----+--------------------+
        +---------------+            |                    |
        |  Suppliers    |            |                    |
        +---------------+            | *                  | *
                            +-------------------+  +-------------------+
                            |   OrderDetails    |  |     Inventory     |
                            +-------------------+  +-------------------+
                                     | *                    | *
                                     |                      |
                                     | 1                    | 1
 +-------------------+      +-------------------+  +-------------------+
 |     Customers     |----->|      Orders       |<---|      Stores       |
 +-------------------+ 1  * +-------------------+ * 1+-------------------+
                                     | *                    | 1
                                     |                      |
                                     | 1                    | *
                            +-------------------+  +-------------------+
                            |     Payments      |  |     Employees     |
                            +-------------------+  +-------------------+
```

## Entity Relationships & Cardinality

| Fact / Dimension Table | Related Table | Relationship Key | Cardinality | Cross Filter Direction |
| :--- | :--- | :--- | :--- | :--- |
| **OrderDetails** (Fact) | **Orders** (Fact/Header) | `OrderID` | Many-to-One (`*:1`) | Single (Orders filters OrderDetails) |
| **OrderDetails** (Fact) | **Products** (Dimension) | `ProductID` | Many-to-One (`*:1`) | Single |
| **Products** (Dimension) | **Categories** (Dimension) | `CategoryID` | Many-to-One (`*:1`) | Single |
| **Products** (Dimension) | **Suppliers** (Dimension) | `SupplierID` | Many-to-One (`*:1`) | Single |
| **Orders** (Header) | **Customers** (Dimension) | `CustomerID` | Many-to-One (`*:1`) | Single |
| **Orders** (Header) | **Stores** (Dimension) | `StoreID` | Many-to-One (`*:1`) | Single |
| **Orders** (Header) | **Employees** (Dimension) | `EmployeeID` | Many-to-One (`*:1`) | Single |
| **Inventory** (Fact) | **Stores** (Dimension) | `StoreID` | Many-to-One (`*:1`) | Single |
| **Inventory** (Fact) | **Products** (Dimension) | `ProductID` | Many-to-One (`*:1`) | Single |
| **Payments** (Fact) | **Orders** (Header) | `OrderID` | Many-to-One (`*:1`) | Single |
| **Returns** (Fact) | **Orders** (Header) | `OrderID` | Many-to-One (`*:1`) | Single |

## Date Table Integration
A dedicated `CalendarDate` table should be created in Power BI using DAX:
```dax
CalendarDate = 
ADDCOLUMNS (
    CALENDAR (DATE(2024, 1, 1), DATE(2026, 12, 31)),
    "Year", YEAR([Date]),
    "MonthNo", MONTH([Date]),
    "Month", FORMAT([Date], "MMM"),
    "YearMonth", FORMAT([Date], "YYYY-MM"),
    "Quarter", "Q" & FORMAT([Date], "Q"),
    "DayOfWeek", FORMAT([Date], "DDD")
)
```
Connect `CalendarDate[Date]` to `Orders[OrderDate]` (1-to-Many).
