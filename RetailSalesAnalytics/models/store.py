from datetime import datetime
from . import db

class Store(db.Model):
    __tablename__ = 'Stores'

    StoreID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    StoreName = db.Column(db.String(100), nullable=False, unique=True)
    Location = db.Column(db.String(200), nullable=False)
    City = db.Column(db.String(100), nullable=False)
    Region = db.Column(db.String(50), nullable=False)
    StoreType = db.Column(db.String(30), default='Flagship')
    ManagerName = db.Column(db.String(100))
    SquareFeet = db.Column(db.Integer)
    OpenedDate = db.Column(db.Date)
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)

    employees = db.relationship('Employee', backref='store', lazy=True)
    orders = db.relationship('Order', backref='store', lazy=True)
    inventory_items = db.relationship('Inventory', backref='store', lazy=True)

    def to_dict(self):
        return {
            'StoreID': self.StoreID,
            'StoreName': self.StoreName,
            'Location': self.Location,
            'City': self.City,
            'Region': self.Region,
            'StoreType': self.StoreType,
            'ManagerName': self.ManagerName,
            'SquareFeet': self.SquareFeet
        }
