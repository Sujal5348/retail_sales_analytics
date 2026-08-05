from datetime import datetime
from . import db

class Payment(db.Model):
    __tablename__ = 'Payments'

    PaymentID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    OrderID = db.Column(db.Integer, db.ForeignKey('Orders.OrderID'), nullable=False)
    PaymentDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    Amount = db.Column(db.Float, nullable=False)
    PaymentMethod = db.Column(db.String(30), nullable=False)
    TransactionStatus = db.Column(db.String(20), default='Success')
    TransactionReference = db.Column(db.String(100), unique=True)

    def to_dict(self):
        return {
            'PaymentID': self.PaymentID,
            'OrderID': self.OrderID,
            'PaymentDate': self.PaymentDate.strftime('%Y-%m-%d %H:%M:%S') if self.PaymentDate else '',
            'Amount': self.Amount,
            'PaymentMethod': self.PaymentMethod,
            'TransactionStatus': self.TransactionStatus,
            'TransactionReference': self.TransactionReference
        }
