from datetime import datetime
from . import db

class Customer(db.Model):
    __tablename__ = 'Customers'

    CustomerID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FirstName = db.Column(db.String(50), nullable=False)
    LastName = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(120), nullable=False, unique=True)
    Phone = db.Column(db.String(30))
    Gender = db.Column(db.String(15))
    Age = db.Column(db.Integer)
    City = db.Column(db.String(100), nullable=False)
    Region = db.Column(db.String(50), nullable=False)
    Segment = db.Column(db.String(30), default='Regular')
    JoinDate = db.Column(db.Date, nullable=False)
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)

    orders = db.relationship('Order', backref='customer', lazy=True)

    @property
    def full_name(self):
        return f"{self.FirstName} {self.LastName}"

    def to_dict(self):
        return {
            'CustomerID': self.CustomerID,
            'CustomerName': self.full_name,
            'Email': self.Email,
            'Phone': self.Phone,
            'Gender': self.Gender,
            'Age': self.Age,
            'City': self.City,
            'Region': self.Region,
            'Segment': self.Segment,
            'JoinDate': self.JoinDate.strftime('%Y-%m-%d') if self.JoinDate else ''
        }
