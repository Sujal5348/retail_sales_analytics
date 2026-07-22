# Power BI Dashboard Specification & Visual Layout Guide

This document specifies the exact layout, visuals, and interactive filters for building the 5 core enterprise Power BI dashboards for the **Retail Sales Analytics System**.

---

## 1. Executive Dashboard (Page 1)
**Target Audience**: C-Suite Executives, Regional Vice Presidents, Store Operations Directors

### Layout Grid:
- **Top Row**: 5 KPI Cards
  1. `Total Revenue` (Formatted: `$#,##0.00`)
  2. `Total Profit` (Formatted: `$#,##0.00` with conditional green formatting)
  3. `Gross Margin %` (Gauge Visual with target 45%)
  4. `Total Active Customers`
  5. `Average Order Value (AOV)`
- **Middle Left**: Line & Clustered Column Chart
  - *X-Axis*: `CalendarDate[YearMonth]`
  - *Column Y-Axis*: `Total Revenue`
  - *Line Y-Axis*: `Revenue YoY Growth %`
- **Middle Right**: Donut Chart
  - *Legend*: `Stores[Region]`
  - *Values*: `Total Revenue`
- **Bottom Left**: Horizontal Bar Chart
  - *Y-Axis*: `Categories[CategoryName]`
  - *X-Axis*: `Total Revenue`
- **Bottom Right**: Matrix Visual
  - *Rows*: `Stores[StoreName]`
  - *Columns*: `Orders[PaymentMethod]`
  - *Values*: `Total Revenue`

---

## 2. Sales Analytics Dashboard (Page 2)
**Target Audience**: Sales Managers, Pricing Analysts

### Visual Components:
1. **Slicers Panel (Top)**: Date Range Picker, Region Dropdown, Store Type, Payment Method.
2. **Sales Trend Area Chart**: Daily & Weekly Revenue trends with 30-day moving average trendlines.
3. **Product Performance Matrix**: Top 25 Products ranked by Revenue, COGS, Profit Margin %, Units Sold, and Return Rate.
4. **Discount Impact Scatter Plot**: Discount % vs. Sales Volume to analyze pricing elasticity.

---

## 3. Customer & CLV Dashboard (Page 3)
**Target Audience**: Marketing Team, Customer Success Managers

### Visual Components:
1. **Customer Segmentation Pie Chart**: Breakdown of VIP, Regular, Occasional, and New Customers.
2. **Customer Lifetime Value (CLV) Histogram**: Distribution of Customer Spend Tiers.
3. **Repeat Purchase Rate Funnel**: New vs. Repeat Customers over time.
4. **Regional Customer Heatmap**: Customer concentration by City and Region.

---

## 4. Inventory & Stock Control Dashboard (Page 4)
**Target Audience**: Supply Chain Director, Inventory Managers, Procurement Specialists

### Visual Components:
1. **Stock Alert KPI Cards**:
   - `Total Inventory Valuation ($)`
   - `Low Stock Items Count`
   - `Out of Stock Items Count`
   - `Inventory Turnover Ratio`
2. **Reorder Alert Table**: Filtered to items where `StockQuantity <= ReorderLevel`, highlighting recommended reorder quantities and supplier emails.
3. **Category Inventory Tree Map**: Valuation of stock grouped by Department and Category.

---

## 5. Regional & Store Performance Dashboard (Page 5)
**Target Audience**: Regional Operations Managers, Franchise Directors

### Visual Components:
1. **Regional Sales Map Visual**: Bubble size proportional to Store Revenue.
2. **Store Target vs. Actual Bar Chart**: Bullet chart showing Store Sales achieved vs Store Monthly Target.
3. **Employee Leaderboard Table**: Top Salespersons ranked by Revenue Achieved with target progress bars.
