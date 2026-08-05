from datetime import datetime
from . import db

class ReturnModel(db.Model):
    __tablename__ = 'Returns'

    ReturnID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    OrderID = db.Column(db.Integer, db.ForeignKey('Orders.OrderID'), nullable=False)
    ProductID = db.Column(db.Integer, db.ForeignKey('Products.ProductID'), nullable=False)
    ReturnDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    Quantity = db.Column(db.Integer, nullable=False)
    Reason = db.Column(db.String(150), nullable=False)
    RefundAmount = db.Column(db.Float, nullable=False)
    Status = db.Column(db.String(20), default='Approved')

    def to_dict(self):
        return {
            'ReturnID': self.ReturnID,
            'OrderID': self.OrderID,
            'ProductID': self.ProductID,
            'ProductName': self.product.ProductName if self.product else '',
            'ReturnDate': self.ReturnDate.strftime('%Y-%m-%d %H:%M:%S') if self.ReturnDate else '',
            'Quantity': self.Quantity,
            'Reason': self.Reason,
            'RefundAmount': self.RefundAmount,
            'Status': self.Status
        }
