from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .category import Category
from .supplier import Supplier
from .product import Product
from .customer import Customer
from .store import Store
from .employee import Employee
from .order import Order
from .order_detail import OrderDetail
from .inventory import Inventory
from .payment import Payment
from .return_model import ReturnModel
