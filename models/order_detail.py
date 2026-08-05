from . import db

class OrderDetail(db.Model):
    __tablename__ = 'OrderDetails'

    OrderDetailID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    OrderID = db.Column(db.Integer, db.ForeignKey('Orders.OrderID'), nullable=False)
    ProductID = db.Column(db.Integer, db.ForeignKey('Products.ProductID'), nullable=False)
    Quantity = db.Column(db.Integer, nullable=False)
    UnitPrice = db.Column(db.Float, nullable=False)
    CostPrice = db.Column(db.Float, nullable=False)
    Discount = db.Column(db.Float, default=0.0)
    Tax = db.Column(db.Float, default=5.0)
    LineTotal = db.Column(db.Float)
    LineProfit = db.Column(db.Float)

    def calculate_totals(self):
        disc_price = self.Quantity * self.UnitPrice * (1 - self.Discount/100.0)
        self.LineTotal = round(disc_price * (1 + self.Tax/100.0), 2)
        self.LineProfit = round(disc_price - (self.Quantity * self.CostPrice), 2)

    def to_dict(self):
        return {
            'OrderDetailID': self.OrderDetailID,
            'OrderID': self.OrderID,
            'ProductID': self.ProductID,
            'ProductName': self.product.ProductName if self.product else '',
            'SKU': self.product.SKU if self.product else '',
            'Quantity': self.Quantity,
            'UnitPrice': self.UnitPrice,
            'CostPrice': self.CostPrice,
            'Discount': self.Discount,
            'Tax': self.Tax,
            'LineTotal': self.LineTotal,
            'LineProfit': self.LineProfit
        }
