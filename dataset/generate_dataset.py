import os
import random
import datetime
import pandas as pd
import numpy as np
from faker import Faker

def generate_all():
    # Initialize Faker with Indian locale for realistic names and contexts
    fake = Faker('en_IN')
    Faker.seed(42)
    random.seed(42)

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    OUTPUT_DIR = os.path.join(BASE_DIR, 'dataset', 'sample_csvs')
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Starting Zudio Fashion Analytics Synthetic Dataset Generation...")

    # 1. Zudio Departments & Categories
    departments = {
        "Men's Wear": ["Men's T-Shirts & Tops", "Men's Shirts", "Men's Bottomwear", "Men's Activewear & Outerwear"],
        "Women's Wear": ["Women's Tops & Tees", "Women's Ethnic Wear", "Women's Bottomwear", "Women's Dresses"],
        "Kids' Wear": ["Boys' Wear", "Girls' Wear", "Infants & Toddlers"],
        "Footwear": ["Men's Footwear", "Women's Footwear", "Unisex Casual Footwear"],
        "Accessories & Cosmetics": ["Deodorants & Perfumes", "Makeup & Cosmetics", "Socks, Bags & Belts"]
    }

    categories_data = []
    cat_id = 1
    for dept, cat_list in departments.items():
        for cat_name in cat_list:
            categories_data.append({
                'CategoryID': cat_id,
                'CategoryName': cat_name,
                'Department': dept,
                'Description': f"Trendy budget-friendly fashion items under {cat_name} in {dept} department."
            })
            cat_id += 1
    df_categories = pd.DataFrame(categories_data)
    df_categories.to_csv(os.path.join(OUTPUT_DIR, 'categories.csv'), index=False)
    print(f"Generated {len(df_categories)} Categories.")

    # 2. Suppliers (50 Indian Apparel & Textile Suppliers)
    suppliers_data = []
    textile_hubs = ['Surat', 'Tiruppur', 'Ludhiana', 'Mumbai', 'Ahmedabad', 'Jaipur', 'Coimbatore', 'Kolkata']
    for i in range(1, 51):
        suppliers_data.append({
            'SupplierID': i,
            'SupplierName': f"{fake.last_name()} Textiles & Apparel Ltd.",
            'ContactName': fake.name(),
            'Email': fake.company_email(),
            'Phone': fake.phone_number(),
            'City': random.choice(textile_hubs),
            'Country': 'India',
            'Rating': round(random.uniform(3.8, 5.0), 2)
        })
    df_suppliers = pd.DataFrame(suppliers_data)
    df_suppliers.to_csv(os.path.join(OUTPUT_DIR, 'suppliers.csv'), index=False)
    print(f"Generated {len(df_suppliers)} Suppliers.")

    # 3. Zudio Products (2,000 Products with budget pricing under ₹999)
    # Zudio price points: 79, 99, 149, 199, 249, 299, 399, 499, 599, 699, 799, 899, 999
    zudio_prices = [79, 99, 149, 199, 249, 299, 399, 499, 599, 699, 799, 899, 999]
    
    adjectives = ['Casual', 'Slim-Fit', 'Regular', 'Printed', 'Solid', 'Classic', 'Sporty', 'Ethnic', 'Denim', 'Stretch', 'Cozy', 'Stylish']
    nouns_by_dept = {
        "Men's Wear": ['T-Shirt', 'Polo T-Shirt', 'Casual Shirt', 'Chino Pants', 'Cargo Shorts', 'Denim Jeans', 'Joggers', 'Hoodie', 'Track Pants'],
        "Women's Wear": ['Graphic Tee', 'Cropped Top', 'Anarkali Kurta', 'Straight Kurti', 'Skinny Jeans', 'Palazzo Pants', 'Maxi Dress', 'Leggings', 'Sports Bra'],
        "Kids' Wear": ['Printed Tee', 'Denim Shorts', 'Frock', 'Jumpsuit', 'Tracksuit', 'Pajama Set'],
        "Footwear": ['Sneakers', 'Slides', 'Running Shoes', 'Flip Flops', 'Flat Sandals', 'Canvas Shoes', 'Loafers'],
        "Accessories & Cosmetics": ['Deodorant Spray', 'Eau de Toilette', 'Matte Lipstick', 'Nail Polish', 'Ankle Socks', 'Canvas Backpack', 'Leather Belt']
    }

    products_data = []
    for i in range(1, 2001):
        cat = random.choice(categories_data)
        dept = cat['Department']
        adj = random.choice(adjectives)
        noun = random.choice(nouns_by_dept[dept])
        p_name = f"Zudio {adj} {noun} {random.randint(10, 99)}"
        
        # Budget pricing rules:
        if dept == "Accessories & Cosmetics":
            price = random.choice([79, 99, 149, 199, 249, 299])
        elif dept == "Kids' Wear":
            price = random.choice([149, 199, 249, 299, 399, 499, 599])
        elif dept == "Footwear":
            price = random.choice([299, 399, 499, 599, 699, 799, 899])
        else: # Men's & Women's wear
            price = random.choice([199, 249, 299, 399, 499, 599, 699, 799, 899, 999])
            
        cost = round(price * random.uniform(0.40, 0.55), 2)
        
        products_data.append({
            'ProductID': i,
            'SKU': f"ZUD-{cat['CategoryID']:02d}-{i:04d}",
            'ProductName': p_name,
            'CategoryID': cat['CategoryID'],
            'SupplierID': random.randint(1, 50),
            'CostPrice': cost,
            'SellingPrice': float(price),
            'Status': 'Active' if random.random() > 0.03 else 'Discontinued'
        })
    df_products = pd.DataFrame(products_data)
    df_products.to_csv(os.path.join(OUTPUT_DIR, 'products.csv'), index=False)
    print(f"Generated {len(df_products)} Products.")

    # 4. Indian Regions & Cities
    regions = {
        'North': ['New Delhi', 'Jaipur', 'Lucknow', 'Chandigarh'],
        'South': ['Bangalore', 'Hyderabad', 'Chennai', 'Kochi'],
        'West': ['Mumbai', 'Pune', 'Ahmedabad', 'Surat'],
        'East': ['Kolkata', 'Patna', 'Bhubaneswar', 'Guwahati'],
        'Central': ['Indore', 'Bhopal', 'Nagpur', 'Raipur']
    }

    # 5. Stores (20 Zudio Stores in India)
    stores_data = []
    store_types = ['Flagship Store', 'Mall Store', 'High Street Store']
    store_id = 1
    for reg, cities in regions.items():
        for city in cities[:4]:
            stores_data.append({
                'StoreID': store_id,
                'StoreName': f"Zudio - {city}",
                'Location': f"{random.randint(10, 99)}, Mall Road, {city}",
                'City': city,
                'Region': reg,
                'StoreType': random.choice(store_types),
                'ManagerName': fake.name(),
                'SquareFeet': random.randint(6000, 18000),
                'OpenedDate': fake.date_between(start_date='-4y', end_date='-1y')
            })
            store_id += 1
    df_stores = pd.DataFrame(stores_data)
    df_stores.to_csv(os.path.join(OUTPUT_DIR, 'stores.csv'), index=False)
    print(f"Generated {len(df_stores)} Stores.")

    # 6. Employees (50 Indian Sales Associates & Managers)
    employees_data = []
    positions = ['Store Manager', 'Assistant Store Manager', 'Senior Cashier', 'Fashion Consultant', 'Retail Associate']
    for i in range(1, 51):
        store = random.choice(stores_data)
        employees_data.append({
            'EmployeeID': i,
            'StoreID': store['StoreID'],
            'FirstName': fake.first_name(),
            'LastName': fake.last_name(),
            'Email': f"{fake.first_name().lower()}.{fake.last_name().lower()}_zudio@trent.in",
            'Position': random.choice(positions),
            'MonthlyTarget': round(random.choice([150000.0, 200000.0, 250000.0, 300000.0]), 2), # targets in INR
            'HireDate': fake.date_between(start_date='-3y', end_date='-3m')
        })
    df_employees = pd.DataFrame(employees_data)
    df_employees.to_csv(os.path.join(OUTPUT_DIR, 'employees.csv'), index=False)
    print(f"Generated {len(df_employees)} Employees.")

    # 7. Customers (10,000 Indian Customers)
    customers_data = []
    segments = ['VIP', 'Regular', 'Occasional', 'New']
    start_join = datetime.date(2023, 1, 1)
    end_join = datetime.date(2026, 6, 1)

    for i in range(1, 10001):
        reg = random.choice(list(regions.keys()))
        city = random.choice(regions[reg])
        j_date = fake.date_between(start_date=start_join, end_date=end_join)
        gender = random.choice(['Male', 'Female', 'Other'])
        customers_data.append({
            'CustomerID': i,
            'FirstName': fake.first_name(),
            'LastName': fake.last_name(),
            'Email': f"cust{i}_{fake.free_email_domain()}",
            'Phone': f"+91 {random.randint(7,9)}{random.randint(10,99)}{random.randint(100,999)}{random.randint(100,999)}",
            'Gender': gender,
            'Age': random.randint(15, 60), # Zudio targets younger crowd
            'City': city,
            'Region': reg,
            'Segment': random.choices(segments, weights=[0.08, 0.42, 0.35, 0.15])[0],
            'JoinDate': j_date
        })
    df_customers = pd.DataFrame(customers_data)
    df_customers.to_csv(os.path.join(OUTPUT_DIR, 'customers.csv'), index=False)
    print(f"Generated {len(df_customers)} Customers.")

    # 8. Orders & OrderDetails (exactly 100,000 details)
    orders_data = []
    order_details_data = []
    payments_data = []
    returns_data = []

    # Indian payment methods: UPI is very popular in Zudio stores, Cash, Debit, Credit
    payment_methods = ['UPI', 'UPI', 'UPI', 'Cash', 'Debit Card', 'Credit Card']
    order_statuses = ['Completed', 'Completed', 'Completed', 'Completed', 'Completed', 'Cancelled']
    return_reasons = ['Wrong Size', 'Changed Mind', 'Fabric Quality', 'Defective Stitching', 'Color Bled']

    order_id = 1
    detail_id = 1
    payment_id = 1
    return_id = 1

    start_sales_date = datetime.datetime(2024, 1, 1)
    end_sales_date = datetime.datetime(2026, 7, 1)
    total_days = (end_sales_date - start_sales_date).days

    print("Generating 100,000 transaction line items across Zudio Orders...")

    # We will generate orders until total order details reaches exactly 100,000
    while detail_id <= 100000:
        cust = random.choice(customers_data)
        store = random.choice(stores_data)
        emp = random.choice([e for e in employees_data if e['StoreID'] == store['StoreID']] or employees_data)
        
        # Pick Date with seasonality (Diwali, Eid, Puja, Year-End boost in India)
        rand_day = random.randint(0, total_days)
        o_date = start_sales_date + datetime.timedelta(days=rand_day, hours=random.randint(10, 22), minutes=random.randint(0, 59))
        
        # Seasonality Multipliers (Oct-Nov Diwali, May Eid/Summer shopping)
        if o_date.month in [10, 11, 12, 5]:
            if random.random() < 0.35:
                rand_day = random.randint(0, total_days)
                o_date = start_sales_date + datetime.timedelta(days=rand_day, hours=random.randint(10, 22))
                
        pm = random.choice(payment_methods)
        status = random.choice(order_statuses)
        
        # Order items per order (between 2 and 7 items for fashion shopping spree)
        items_count = random.randint(2, 7)
        if detail_id + items_count > 100000:
            items_count = 100000 - detail_id + 1
            
        order_total = 0.0
        order_tax = 0.0
        order_discount = 0.0
        
        selected_products = random.sample(products_data, items_count)
        
        for prod in selected_products:
            qty = random.randint(1, 3)
            unit_price = prod['SellingPrice']
            cost_price = prod['CostPrice']
            
            # Zudio has a flat low-pricing model, discounts are rare (maybe end-of-season sale 10%)
            disc_pct = random.choice([0.0, 0.0, 0.0, 0.0, 0.0, 10.0])
            tax_pct = 5.0 # GST for apparel in budget tier is generally 5%
            
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
            
            # Apparel Return Logic (~5% return probability due to fit issues in apparel retail)
            if status == 'Completed' and random.random() < 0.05:
                ret_date = o_date + datetime.timedelta(days=random.randint(1, 7))
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
            'TransactionReference': f"TXN-ZUD-{order_id:06d}-{payment_id:06d}"
        })
        
        payment_id += 1
        order_id += 1

    # 9. Inventory Data (Stores x Products)
    print("Generating Zudio Store Inventory Stock Levels...")
    inventory_data = []
    inv_id = 1
    for st in stores_data:
        for pr in products_data:
            stock = random.randint(10, 200) # Fashion stores keep slightly higher floor stock
            inventory_data.append({
                'InventoryID': inv_id,
                'StoreID': st['StoreID'],
                'ProductID': pr['ProductID'],
                'StockQuantity': stock,
                'ReorderLevel': 25,
                'LastRestockDate': fake.date_between(start_date='-2m', end_date='today').strftime('%Y-%m-%d %H:%M:%S')
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

    print("\n--- Zudio Fashion Dataset Generation Complete ---")
    print(f"Orders: {len(df_orders):,}")
    print(f"Order Details (Transactions): {len(df_order_details):,}")
    print(f"Customers: {len(df_customers):,}")
    print(f"Products: {len(df_products):,}")
    print(f"Inventory Stock Entries: {len(df_inventory):,}")
    print(f"Payments: {len(df_payments):,}")
    print(f"Returns: {len(df_returns):,}")

if __name__ == '__main__':
    generate_all()
