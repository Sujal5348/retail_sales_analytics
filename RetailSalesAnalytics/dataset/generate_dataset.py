import os
import random
import datetime
import pandas as pd
import numpy as np
from faker import Faker

# Initialize Faker
fake = Faker()
Faker.seed(42)
random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, 'dataset', 'sample_csvs')
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Starting Retail Analytics Synthetic Dataset Generation...")

# 1. Categories (15 categories across 4 departments)
departments = {
    'Electronics': ['Smartphones & Tablets', 'Laptops & Computers', 'Audio & Headphones', 'Smart Home & Wearables'],
    'Apparel': ['Men\'s Fashion', 'Women\'s Fashion', 'Footwear', 'Activewear & Sportswear'],
    'Home & Kitchen': ['Furniture', 'Kitchenware & Appliances', 'Home Decor', 'Bedding & Bath'],
    'Beauty & Health': ['Skincare & Cosmetics', 'Haircare', 'Personal Wellness']
}

categories_data = []
cat_id = 1
for dept, cat_list in departments.items():
    for cat_name in cat_list:
        categories_data.append({
            'CategoryID': cat_id,
            'CategoryName': cat_name,
            'Department': dept,
            'Description': f"High-quality retail items under {cat_name} in {dept} department."
        })
        cat_id += 1
df_categories = pd.DataFrame(categories_data)
df_categories.to_csv(os.path.join(OUTPUT_DIR, 'categories.csv'), index=False)
print(f"Generated {len(df_categories)} Categories.")

# 2. Suppliers (50 Suppliers)
suppliers_data = []
for i in range(1, 51):
    suppliers_data.append({
        'SupplierID': i,
        'SupplierName': f"{fake.company()} Direct",
        'ContactName': fake.name(),
        'Email': fake.company_email(),
        'Phone': fake.phone_number(),
        'City': fake.city(),
        'Country': 'USA',
        'Rating': round(random.uniform(3.5, 5.0), 2)
    })
df_suppliers = pd.DataFrame(suppliers_data)
df_suppliers.to_csv(os.path.join(OUTPUT_DIR, 'suppliers.csv'), index=False)
print(f"Generated {len(df_suppliers)} Suppliers.")

# 3. Products (2,000 Products)
products_data = []
adjectives = ['Ultra', 'Pro', 'Lite', 'Smart', 'Eco', 'Classic', 'Premium', 'Ergonomic', 'Compact', 'Elite']
nouns_by_dept = {
    'Electronics': ['Phone', 'Tablet', 'Headphones', 'Speaker', 'Monitor', 'Charger', 'Camera', 'Watch', 'Router', 'Drone'],
    'Apparel': ['Jacket', 'Sneakers', 'T-Shirt', 'Jeans', 'Hoodie', 'Dress', 'Boots', 'Shorts', 'Sweater', 'Coat'],
    'Home & Kitchen': ['Blender', 'Chair', 'Lamp', 'Cookware Set', 'Desk', 'Air Purifier', 'Vacuum', 'Rug', 'Coffee Maker', 'Sofa'],
    'Beauty & Health': ['Serume', 'Moisturizer', 'Massage Gun', 'Shampoo', 'Perfume', 'Vitamin Pack', 'Face Mask', 'Hair Dryer', 'Sunscreen', 'Trimmer']
}

for i in range(1, 2001):
    cat = random.choice(categories_data)
    dept = cat['Department']
    adj = random.choice(adjectives)
    noun = random.choice(nouns_by_dept[dept])
    brand = fake.company().split()[0]
    p_name = f"{brand} {adj} {noun} {random.randint(100, 999)}"
    
    # Cost & Price Math
    cost = round(random.uniform(5.0, 450.0), 2)
    markup = random.uniform(1.3, 2.5)
    price = round(cost * markup, 2)
    
    products_data.append({
        'ProductID': i,
        'SKU': f"SKU-{cat['CategoryID']:02d}-{i:04d}",
        'ProductName': p_name,
        'CategoryID': cat['CategoryID'],
        'SupplierID': random.randint(1, 50),
        'CostPrice': cost,
        'SellingPrice': price,
        'Status': 'Active' if random.random() > 0.05 else 'Discontinued'
    })
df_products = pd.DataFrame(products_data)
df_products.to_csv(os.path.join(OUTPUT_DIR, 'products.csv'), index=False)
print(f"Generated {len(df_products)} Products.")

# 4. Regions & Cities
regions = {
    'North': ['New York', 'Boston', 'Chicago', 'Philadelphia'],
    'South': ['Houston', 'Atlanta', 'Dallas', 'Miami'],
    'West': ['Los Angeles', 'Seattle', 'San Francisco', 'Phoenix'],
    'Midwest': ['Indianapolis', 'Columbus', 'Detroit', 'Minneapolis'],
    'East': ['Washington DC', 'Baltimore', 'Charlotte', 'Orlando']
}

# 5. Stores (20 Stores)
stores_data = []
store_types = ['Flagship', 'Standard', 'Outlet', 'Express']
store_id = 1
for reg, cities in regions.items():
    for city in cities[:4]:
        stores_data.append({
            'StoreID': store_id,
            'StoreName': f"Apex Retail - {city}",
            'Location': f"{random.randint(100, 999)} {fake.street_name()}",
            'City': city,
            'Region': reg,
            'StoreType': random.choice(store_types),
            'ManagerName': fake.name(),
            'SquareFeet': random.randint(3000, 25000),
            'OpenedDate': fake.date_between(start_date='-5y', end_date='-2y')
        })
        store_id += 1
df_stores = pd.DataFrame(stores_data)
df_stores.to_csv(os.path.join(OUTPUT_DIR, 'stores.csv'), index=False)
print(f"Generated {len(df_stores)} Stores.")

# 6. Employees (50 Employees)
employees_data = []
positions = ['Store Manager', 'Assistant Manager', 'Senior Sales Associate', 'Sales Associate']
for i in range(1, 51):
    employees_data.append({
        'EmployeeID': i,
        'StoreID': random.randint(1, len(stores_data)),
        'FirstName': fake.first_name(),
        'LastName': fake.last_name(),
        'Email': fake.unique.email(),
        'Position': random.choice(positions),
        'MonthlyTarget': round(random.choice([30000.0, 45000.0, 60000.0, 75000.0]), 2),
        'HireDate': fake.date_between(start_date='-4y', end_date='-6m')
    })
df_employees = pd.DataFrame(employees_data)
df_employees.to_csv(os.path.join(OUTPUT_DIR, 'employees.csv'), index=False)
print(f"Generated {len(df_employees)} Employees.")

# 7. Customers (10,000 Customers)
customers_data = []
segments = ['VIP', 'Regular', 'Occasional', 'New']
all_cities = [c for cities in regions.values() for c in cities]

start_join = datetime.date(2023, 1, 1)
end_join = datetime.date(2026, 6, 1)

for i in range(1, 10001):
    reg = random.choice(list(regions.keys()))
    city = random.choice(regions[reg])
    j_date = fake.date_between(start_date=start_join, end_date=end_join)
    customers_data.append({
        'CustomerID': i,
        'FirstName': fake.first_name(),
        'LastName': fake.last_name(),
        'Email': f"cust{i}_{fake.domain_name()}",
        'Phone': fake.phone_number(),
        'Gender': random.choice(['Male', 'Female', 'Other']),
        'Age': random.randint(18, 72),
        'City': city,
        'Region': reg,
        'Segment': random.choices(segments, weights=[0.1, 0.4, 0.35, 0.15])[0],
        'JoinDate': j_date
    })
df_customers = pd.DataFrame(customers_data)
df_customers.to_csv(os.path.join(OUTPUT_DIR, 'customers.csv'), index=False)
print(f"Generated {len(df_customers)} Customers.")

# 8. Orders & OrderDetails (~25,000 Orders yielding 100,000 OrderDetails)
orders_data = []
order_details_data = []
payments_data = []
returns_data = []

payment_methods = ['Credit Card', 'Debit Card', 'Cash', 'UPI', 'PayPal', 'Gift Card']
order_statuses = ['Completed', 'Completed', 'Completed', 'Completed', 'Completed', 'Cancelled']
return_reasons = ['Defective Item', 'Wrong Size', 'Changed Mind', 'Not as Pictured', 'Late Delivery']

order_id = 1
detail_id = 1
payment_id = 1
return_id = 1

start_sales_date = datetime.datetime(2024, 1, 1)
end_sales_date = datetime.datetime(2026, 7, 1)
total_days = (end_sales_date - start_sales_date).days

print("Generating 100,000 transaction line items across Orders...")

# We will generate orders until total order details reaches 100,000
while detail_id <= 100000:
    cust = random.choice(customers_data)
    store = random.choice(stores_data)
    emp = random.choice([e for e in employees_data if e['StoreID'] == store['StoreID']] or employees_data)
    
    # Pick Date with seasonality (Q4 boost)
    rand_day = random.randint(0, total_days)
    o_date = start_sales_date + datetime.timedelta(days=rand_day, hours=random.randint(8, 21), minutes=random.randint(0, 59))
    if o_date.month in [11, 12]: # Q4 seasonality multiplier
        if random.random() < 0.3:
            rand_day = random.randint(0, total_days)
            o_date = start_sales_date + datetime.timedelta(days=rand_day, hours=random.randint(8, 21))
            
    pm = random.choice(payment_methods)
    status = random.choice(order_statuses)
    
    # Order items per order (between 2 and 6 items)
    items_count = random.randint(2, 6)
    if detail_id + items_count > 100000:
        items_count = 100000 - detail_id + 1
        
    order_total = 0.0
    order_tax = 0.0
    order_discount = 0.0
    
    selected_products = random.sample(products_data, items_count)
    
    for prod in selected_products:
        qty = random.randint(1, 4)
        unit_price = prod['SellingPrice']
        cost_price = prod['CostPrice']
        disc_pct = random.choice([0.0, 0.0, 0.0, 5.0, 10.0, 15.0, 20.0])
        tax_pct = 5.0
        
        line_price_disc = qty * unit_price * (1 - disc_pct / 100.0)
        line_tax = line_price_disc * (tax_pct / 100.0)
        line_total = line_price_disc + line_tax
        line_profit = line_price_disc - (qty * cost_price)
        
        order_total += line_total
        order_tax += line_tax
        order_discount += (qty * unit_price * (disc_pct / 100.0))
        
        order_details_data.append({
            'OrderDetailID': detail_id,
            'OrderID': order_id,
            'ProductID': prod['ProductID'],
            'Quantity': qty,
            'UnitPrice': unit_price,
            'CostPrice': cost_price,
            'Discount': disc_pct,
            'Tax': tax_pct,
            'LineTotal': round(line_total, 2),
            'LineProfit': round(line_profit, 2)
        })
        
        # Product Return Logic (~4% return probability for completed orders)
        if status == 'Completed' and random.random() < 0.04:
            ret_date = o_date + datetime.timedelta(days=random.randint(1, 14))
            returns_data.append({
                'ReturnID': return_id,
                'OrderID': order_id,
                'ProductID': prod['ProductID'],
                'ReturnDate': ret_date.strftime('%Y-%m-%d %H:%M:%S'),
                'Quantity': random.randint(1, qty),
                'Reason': random.choice(return_reasons),
                'RefundAmount': round(line_total, 2),
                'Status': 'Approved'
            })
            return_id += 1
            
        detail_id += 1

    orders_data.append({
        'OrderID': order_id,
        'CustomerID': cust['CustomerID'],
        'StoreID': store['StoreID'],
        'EmployeeID': emp['EmployeeID'],
        'OrderDate': o_date.strftime('%Y-%m-%d %H:%M:%S'),
        'PaymentMethod': pm,
        'Status': status,
        'TotalAmount': round(order_total, 2),
        'DiscountAmount': round(order_discount, 2),
        'TaxAmount': round(order_tax, 2)
    })
    
    # Payment record
    payments_data.append({
        'PaymentID': payment_id,
        'OrderID': order_id,
        'PaymentDate': o_date.strftime('%Y-%m-%d %H:%M:%S'),
        'Amount': round(order_total, 2),
        'PaymentMethod': pm,
        'TransactionStatus': 'Success' if status == 'Completed' else 'Failed',
        'TransactionReference': f"TXN-{order_id:06d}-{payment_id:06d}"
    })
    
    payment_id += 1
    order_id += 1

# 9. Inventory Data (Stores x Products)
print("Generating Inventory Stock Levels...")
inventory_data = []
inv_id = 1
for st in stores_data:
    for pr in products_data:
        stock = random.randint(0, 150)
        inventory_data.append({
            'InventoryID': inv_id,
            'StoreID': st['StoreID'],
            'ProductID': pr['ProductID'],
            'StockQuantity': stock,
            'ReorderLevel': 20,
            'LastRestockDate': fake.date_between(start_date='-3m', end_date='today').strftime('%Y-%m-%d %H:%M:%S')
        })
        inv_id += 1

# Export to CSV
df_orders = pd.DataFrame(orders_data)
df_order_details = pd.DataFrame(order_details_data)
df_inventory = pd.DataFrame(inventory_data)
df_payments = pd.DataFrame(payments_data)
df_returns = pd.DataFrame(returns_data)

df_orders.to_csv(os.path.join(OUTPUT_DIR, 'orders.csv'), index=False)
df_order_details.to_csv(os.path.join(OUTPUT_DIR, 'order_details.csv'), index=False)
df_inventory.to_csv(os.path.join(OUTPUT_DIR, 'inventory.csv'), index=False)
df_payments.to_csv(os.path.join(OUTPUT_DIR, 'payments.csv'), index=False)
df_returns.to_csv(os.path.join(OUTPUT_DIR, 'returns.csv'), index=False)

print("\n--- Synthetic Dataset Generation Complete ---")
print(f"Orders: {len(df_orders):,}")
print(f"Order Details (Transactions): {len(df_order_details):,}")
print(f"Customers: {len(df_customers):,}")
print(f"Products: {len(df_products):,}")
print(f"Inventory Stock Entries: {len(df_inventory):,}")
print(f"Payments: {len(df_payments):,}")
print(f"Returns: {len(df_returns):,}")
