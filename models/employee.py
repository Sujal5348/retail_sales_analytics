from datetime import datetime
from . import db

class Employee(db.Model):
    __tablename__ = 'Employees'

    EmployeeID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    StoreID = db.Column(db.Integer, db.ForeignKey('Stores.StoreID'), nullable=False)
    FirstName = db.Column(db.String(50), nullable=False)
    LastName = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(120), nullable=False, unique=True)
    Position = db.Column(db.String(50), nullable=False)
    MonthlyTarget = db.Column(db.Float, default=50000.0)
    HireDate = db.Column(db.Date, nullable=False)
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)

    orders = db.relationship('Order', backref='employee', lazy=True)

    @property
    def full_name(self):
        return f"{self.FirstName} {self.LastName}"

    def to_dict(self):
        return {
            'EmployeeID': self.EmployeeID,
            'StoreID': self.StoreID,
            'StoreName': self.store.StoreName if self.store else '',
            'EmployeeName': self.full_name,
            'Email': self.Email,
            'Position': self.Position,
            'MonthlyTarget': self.MonthlyTarget,
            'HireDate': self.HireDate.strftime('%Y-%m-%d') if self.HireDate else ''
        }
