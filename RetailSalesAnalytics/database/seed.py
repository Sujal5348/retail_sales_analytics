import os
import sys
import pandas as pd
from sqlalchemy import create_engine, text

# Add parent dir to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from config import Config
from models import db
from app import create_app

def seed_database():
    app = create_app()
    csv_dir = os.path.join(BASE_DIR, 'dataset', 'sample_csvs')
    
    if not os.path.exists(os.path.join(csv_dir, 'orders.csv')):
        print("CSV files not found. Generating synthetic dataset first...")
        from dataset.generate_dataset import generate_all
        generate_all()
        
    print("Seeding database tables from CSV files...")
    
    with app.app_context():
        # Create all tables first
        db.create_all()
        engine = db.engine
        
        # Table mapping order (preserving FK integrity)
        tables_in_order = [
            ('categories.csv', 'Categories'),
            ('suppliers.csv', 'Suppliers'),
            ('products.csv', 'Products'),
            ('stores.csv', 'Stores'),
            ('employees.csv', 'Employees'),
            ('customers.csv', 'Customers'),
            ('orders.csv', 'Orders'),
            ('order_details.csv', 'OrderDetails'),
            ('inventory.csv', 'Inventory'),
            ('payments.csv', 'Payments'),
            ('returns.csv', 'Returns')
        ]
        
        for csv_file, table_name in tables_in_order:
            file_path = os.path.join(csv_dir, csv_file)
            if os.path.exists(file_path):
                print(f"Loading {csv_file} into '{table_name}'...")
                df = pd.read_csv(file_path)
                
                # Format datetime columns appropriately
                for col in df.columns:
                    if col in ['JoinDate', 'OpenedDate', 'HireDate']:
                        df[col] = pd.to_datetime(df[col]).dt.strftime('%Y-%m-%d')
                    elif 'Date' in col:
                        df[col] = pd.to_datetime(df[col]).dt.strftime('%Y-%m-%d %H:%M:%S')
                
                # Fast chunked insertion using pandas
                df.to_sql(table_name, con=engine, if_exists='append', index=False, chunksize=5000)
                print(f"Loaded {len(df):,} rows into {table_name}.")
            else:
                print(f"Warning: {csv_file} not found!")

        print("\nDatabase Seeding Complete Successfully!")

if __name__ == '__main__':
    seed_database()
