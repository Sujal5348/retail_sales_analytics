from datetime import datetime
from . import db

class Order(db.Model):
    __tablename__ = 'Orders'

    OrderID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CustomerID = db.Column(db.Integer, db.ForeignKey('Customers.CustomerID'), nullable=False)
    StoreID = db.Column(db.Integer, db.ForeignKey('Stores.StoreID'), nullable=False)
    EmployeeID = db.Column(db.Integer, db.ForeignKey('Employees.EmployeeID'), nullable=False)
    OrderDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    PaymentMethod = db.Column(db.String(30), nullable=False)
    Status = db.Column(db.String(20), default='Completed')
    TotalAmount = db.Column(db.Float, default=0.0)
    DiscountAmount = db.Column(db.Float, default=0.0)
    TaxAmount = db.Column(db.Float, default=0.0)
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)

    order_details = db.relationship('OrderDetail', backref='order', lazy=True, cascade="all, delete-orphan")
    payments = db.relationship('Payment', backref='order', lazy=True, cascade="all, delete-orphan")
    returns = db.relationship('ReturnModel', backref='order', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'OrderID': self.OrderID,
            'CustomerID': self.CustomerID,
            'CustomerName': self.customer.full_name if self.customer else '',
            'StoreID': self.StoreID,
            'StoreName': self.store.StoreName if self.store else '',
            'EmployeeID': self.EmployeeID,
            'EmployeeName': self.employee.full_name if self.employee else '',
            'OrderDate': self.OrderDate.strftime('%Y-%m-%d %H:%M:%S') if self.OrderDate else '',
            'PaymentMethod': self.PaymentMethod,
            'Status': self.Status,
            'TotalAmount': self.TotalAmount,
            'DiscountAmount': self.DiscountAmount,
            'TaxAmount': self.TaxAmount
        }
