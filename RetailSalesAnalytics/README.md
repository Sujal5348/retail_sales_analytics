# Retail Sales Analytics System 🛒📊

An end-to-end enterprise **Retail Sales Analytics System** designed to solve real-world retail business problems using **Python (Flask, SQLAlchemy, Pandas, Plotly)**, **MySQL / SQLite**, and **Power BI**.

---

## 🌟 Key Features

- **Relational Database Design**: 11 normalized tables (`Customers`, `Products`, `Categories`, `Suppliers`, `Stores`, `Employees`, `Orders`, `OrderDetails`, `Inventory`, `Payments`, `Returns`).
- **Advanced SQL Analytics**: Comprehensive SQL suite implementing `INNER/LEFT/RIGHT JOIN`, `GROUP BY`, `HAVING`, `CASE`, Subqueries, CTEs, Window Functions (`ROW_NUMBER`, `RANK`, `LAG`, `LEAD`, `SUM OVER`), Views, Stored Procedures, and Triggers.
- **Realistic Dataset Generation**: Python synthetic data generator creating **100,000 sales transactions**, 10,000 customers, 2,000 products, 20 stores across 5 regions over 2 full years of sales history.
- **Interactive Flask Web Application**:
  - Executive KPI Overview Dashboard with interactive Plotly.js charts.
  - Sales & Order Management with dynamic line-item order creation modal and order detail viewer.
  - Customer Directory & Customer Lifetime Value (CLV) RFM segmentation.
  - Inventory Valuation, Stock Movement & Low Stock Alerts.
  - Store & Regional performance analysis.
  - Employee sales quota target leaderboard.
  - **Interactive SQL Analytics Studio** for executing custom or prebuilt CTE/Window queries with dynamic table rendering.
- **Automated Reporting**: Multi-tab styled Excel report generator (`openpyxl`) and CSV exporter.
- **Power BI Integration**: 20+ DAX measures, star schema relational model documentation, and visual layout guides for 5 enterprise dashboards.

---

## 🏗️ Technology Stack

- **Backend Framework**: Python (Flask)
- **ORM & Database**: SQLAlchemy, SQLite (Default out-of-the-box), MySQL compatible (`pymysql`)
- **Data Analysis**: Pandas, NumPy
- **Data Visualization**: Plotly.js, Matplotlib, Seaborn
- **Reporting**: OpenPyXL
- **Frontend**: HTML5, CSS3, Bootstrap 5, FontAwesome
- **Business Intelligence**: Power BI (DAX, Star Schema)

---

## 📁 Directory Structure

```
RetailSalesAnalytics/
│
├── app.py                      # Flask Application Entry Point
├── config.py                   # System & Database Configuration
├── requirements.txt            # Python Dependencies
├── database/
│   ├── connection.py           # Database Engine & Sessions
│   └── seed.py                 # Automated CSV Seeder Script
├── models/                     # SQLAlchemy Models (11 Tables)
│   ├── category.py
│   ├── supplier.py
│   ├── product.py
│   ├── customer.py
│   ├── store.py
│   ├── employee.py
│   ├── order.py
│   ├── order_detail.py
│   ├── inventory.py
│   ├── payment.py
│   └── return_model.py
├── routes/                     # Blueprint API & Page Controllers
│   ├── main.py
│   ├── sales.py
│   ├── customers.py
│   ├── inventory.py
│   ├── stores.py
│   ├── employees.py
│   └── analytics_api.py
├── analytics/                  # Core Retail Math & EDA
│   ├── kpi_calculator.py
│   └── eda_engine.py
├── reports/                    # Automated Exporters
│   └── report_generator.py
├── dashboards/                 # Power BI Package
│   ├── DAX_Measures.dax
│   ├── PowerBI_DataModel.md
│   └── PowerBI_Dashboard_Guide.md
├── static/                     # Web Assets (CSS, JS)
│   ├── css/style.css
│   └── js/main.js
├── templates/                  # Jinja2 Templates (Bootstrap 5)
│   ├── base.html
│   ├── dashboard.html
│   ├── sales.html
│   ├── customers.html
│   ├── inventory.html
│   ├── stores.html
│   ├── employees.html
│   ├── analytics.html
│   └── reports.html
├── dataset/                    # Synthetic Data Generator & CSVs
│   ├── generate_dataset.py
│   └── sample_csvs/
└── sql/                        # Advanced MySQL Scripts
    ├── 01_schema.sql
    ├── 02_views.sql
    ├── 03_stored_procedures.sql
    ├── 04_triggers.sql
    └── 05_analytics_queries.sql
```

---

## 🚀 Setup & Execution Guide

### 1. Prerequisites
Ensure Python 3.9+ is installed on your system.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Generate Synthetic Dataset (100,000 Transactions)
```bash
python dataset/generate_dataset.py
```
This generates all CSV files under `dataset/sample_csvs/`.

### 4. Seed Database
```bash
python database/seed.py
```
This loads all CSV data into `database/retail_analytics.db` (or MySQL if configured in `config.py`).

### 5. Launch Web Application
```bash
python app.py
```
Open your browser and navigate to: **`http://localhost:5000`**

---

## 📊 Core Business Questions Answered via SQL

All analytical queries are located in `sql/05_analytics_queries.sql` and accessible via the web app's **SQL Studio**:
1. **Top 10 Selling Products** by Revenue & Profit.
2. **Monthly Sales Trends & MoM Growth Rate** using `LAG()` window functions.
3. **Customer Lifetime Value (CLV)** & RFM Segmentation using `CASE` statements and subqueries.
4. **Store Leaderboard** with running total revenue using `SUM() OVER(PARTITION BY Region)`.
5. **Employee Target Achievement Ranking** using `RANK()`.
6. **Low Stock Alerts & Reorder Valuation**.
7. **Product Return Rates & Refund Impact**.
8. **Customer Retention Rate** (Repeat vs. One-time buyers).

---

## 🎨 Power BI Integration

Import the seeded database or CSV files into Power BI Desktop:
1. Refer to `dashboards/PowerBI_DataModel.md` to establish relationships between tables.
2. Copy and paste measures from `dashboards/DAX_Measures.dax`.
3. Follow `dashboards/PowerBI_Dashboard_Guide.md` to construct the Executive, Sales, Customer, Inventory, and Regional dashboards.

---

## 📜 License
MIT License - Open for Portfolio & Commercial Showcase.
