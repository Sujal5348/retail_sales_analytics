from datetime import datetime
from . import db

class Inventory(db.Model):
    __tablename__ = 'Inventory'

    InventoryID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    StoreID = db.Column(db.Integer, db.ForeignKey('Stores.StoreID'), nullable=False)
    ProductID = db.Column(db.Integer, db.ForeignKey('Products.ProductID'), nullable=False)
    StockQuantity = db.Column(db.Integer, nullable=False, default=0)
    ReorderLevel = db.Column(db.Integer, nullable=False, default=20)
    LastRestockDate = db.Column(db.DateTime, default=datetime.utcnow)
    UpdatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('StoreID', 'ProductID', name='_store_product_uc'),)

    @property
    def status(self):
        if self.StockQuantity == 0:
            return 'Out of Stock'
        elif self.StockQuantity <= self.ReorderLevel:
            return 'Low Stock'
        return 'In Stock'

    def to_dict(self):
        return {
            'InventoryID': self.InventoryID,
            'StoreID': self.StoreID,
            'StoreName': self.store.StoreName if self.store else '',
            'ProductID': self.ProductID,
            'ProductName': self.product.ProductName if self.product else '',
            'SKU': self.product.SKU if self.product else '',
            'StockQuantity': self.StockQuantity,
            'ReorderLevel': self.ReorderLevel,
            'Status': self.status,
            'LastRestockDate': self.LastRestockDate.strftime('%Y-%m-%d %H:%M:%S') if self.LastRestockDate else ''
        }
