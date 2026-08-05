from datetime import datetime
from . import db

class Supplier(db.Model):
    __tablename__ = 'Suppliers'

    SupplierID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    SupplierName = db.Column(db.String(150), nullable=False)
    ContactName = db.Column(db.String(100))
    Email = db.Column(db.String(120), unique=True)
    Phone = db.Column(db.String(30))
    City = db.Column(db.String(100))
    Country = db.Column(db.String(100), default='USA')
    Rating = db.Column(db.Float, default=4.0)
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)

    products = db.relationship('Product', backref='supplier', lazy=True)

    def to_dict(self):
        return {
            'SupplierID': self.SupplierID,
            'SupplierName': self.SupplierName,
            'ContactName': self.ContactName,
            'Email': self.Email,
            'Phone': self.Phone,
            'City': self.City,
            'Country': self.Country,
            'Rating': self.Rating
        }
