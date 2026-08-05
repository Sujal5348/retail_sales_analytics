from datetime import datetime
from . import db

class Product(db.Model):
    __tablename__ = 'Products'

    ProductID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    SKU = db.Column(db.String(50), nullable=False, unique=True)
    ProductName = db.Column(db.String(200), nullable=False)
    CategoryID = db.Column(db.Integer, db.ForeignKey('Categories.CategoryID'), nullable=False)
    SupplierID = db.Column(db.Integer, db.ForeignKey('Suppliers.SupplierID'), nullable=False)
    CostPrice = db.Column(db.Float, nullable=False)
    SellingPrice = db.Column(db.Float, nullable=False)
    Status = db.Column(db.String(20), default='Active')
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)

    order_details = db.relationship('OrderDetail', backref='product', lazy=True)
    inventory_items = db.relationship('Inventory', backref='product', lazy=True)
    returns = db.relationship('ReturnModel', backref='product', lazy=True)

    @property
    def margin_percent(self):
        if self.SellingPrice and self.SellingPrice > 0:
            return round(((self.SellingPrice - self.CostPrice) / self.SellingPrice) * 100, 2)
        return 0.0

    def to_dict(self):
        return {
            'ProductID': self.ProductID,
            'SKU': self.SKU,
            'ProductName': self.ProductName,
            'CategoryID': self.CategoryID,
            'CategoryName': self.category.CategoryName if self.category else '',
            'SupplierID': self.SupplierID,
            'CostPrice': self.CostPrice,
            'SellingPrice': self.SellingPrice,
            'MarginPercent': self.margin_percent,
            'Status': self.Status
        }
