import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'retail-analytics-super-secret-key-2026')
    
    # DB Engine Selection: 'sqlite' or 'mysql'
    DB_ENGINE = os.environ.get('DB_ENGINE', 'sqlite').lower()
    
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'password')
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_PORT = os.environ.get('MYSQL_PORT', '3306')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'retail_sales_db')
    
    SQLITE_PATH = os.path.join(BASE_DIR, 'database', 'retail_analytics.db')
    
    if DB_ENGINE == 'mysql':
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    else:
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{SQLITE_PATH}"
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Analytics config
    EXPORT_FOLDER = os.path.join(BASE_DIR, 'reports', 'exports')
    DATASET_FOLDER = os.path.join(BASE_DIR, 'dataset')
