from datetime import datetime
from . import db

class Category(db.Model):
    __tablename__ = 'Categories'

    CategoryID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CategoryName = db.Column(db.String(100), nullable=False, unique=True)
    Department = db.Column(db.String(100), nullable=False)
    Description = db.Column(db.Text, nullable=True)
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)

    products = db.relationship('Product', backref='category', lazy=True)

    def to_dict(self):
        return {
            'CategoryID': self.CategoryID,
            'CategoryName': self.CategoryName,
            'Department': self.Department,
            'Description': self.Description
        }
