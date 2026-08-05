from flask import Blueprint, render_template, request, jsonify
from models import db, Order, OrderDetail, Customer, Product, Store, Employee, Inventory, Payment
from datetime import datetime

sales_bp = Blueprint('sales', __name__)

@sales_bp.route('/')
def sales_list():
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '', type=str)
    
    query = Order.query
    if status_filter:
        query = query.filter(Order.Status == status_filter)
        
    orders_pagination = query.order_by(Order.OrderDate.desc()).paginate(page=page, per_page=20, error_out=False)
    
    customers = Customer.query.order_by(Customer.FirstName).all()
    stores = Store.query.all()
    employees = Employee.query.all()
    products = Product.query.filter_by(Status='Active').all()

    return render_template('sales.html', 
                           orders=orders_pagination.items, 
                           pagination=orders_pagination,
                           customers=customers,
                           stores=stores,
                           employees=employees,
                           products=products,
                           current_status=status_filter)

@sales_bp.route('/api/order/<int:order_id>')
def order_detail_api(order_id):
    order = Order.query.get_or_404(order_id)
    details = [d.to_dict() for d in order.order_details]
    payments = [p.to_dict() for p in order.payments]
    returns = [r.to_dict() for r in order.returns]
    
    data = order.to_dict()
    data['items'] = details
    data['payments'] = payments
    data['returns'] = returns
    return jsonify(data)

@sales_bp.route('/create', methods=['POST'])
def create_order():
    try:
        data = request.json
        customer_id = data.get('customer_id')
        store_id = data.get('store_id')
        employee_id = data.get('employee_id')
        payment_method = data.get('payment_method', 'Credit Card')
        items = data.get('items', [])
        
        if not items:
            return jsonify({'success': False, 'message': 'No products in order!'}), 400
            
        new_order = Order(
            CustomerID=customer_id,
            StoreID=store_id,
            EmployeeID=employee_id,
            OrderDate=datetime.utcnow(),
            PaymentMethod=payment_method,
            Status='Completed',
            TotalAmount=0.0,
            DiscountAmount=0.0,
            TaxAmount=0.0
        )
        db.session.add(new_order)
        db.session.flush() # Get new_order.OrderID
        
        total_amount = 0.0
        total_tax = 0.0
        total_discount = 0.0
        
        for item in items:
            prod_id = item['product_id']
            qty = int(item['quantity'])
            disc = float(item.get('discount', 0.0))
            tax = 5.0
            
            product = Product.query.get(prod_id)
            if not product:
                continue
                
            unit_price = product.SellingPrice
            cost_price = product.CostPrice
            
            disc_price = qty * unit_price * (1 - disc/100.0)
            line_tax = disc_price * (tax / 100.0)
            line_total = disc_price + line_tax
            line_profit = disc_price - (qty * cost_price)
            
            total_amount += line_total
            total_tax += line_tax
            total_discount += (qty * unit_price * (disc/100.0))
            
            od = OrderDetail(
                OrderID=new_order.OrderID,
                ProductID=prod_id,
                Quantity=qty,
                UnitPrice=unit_price,
                CostPrice=cost_price,
                Discount=disc,
                Tax=tax,
                LineTotal=round(line_total, 2),
                LineProfit=round(line_profit, 2)
            )
            db.session.add(od)
            
            # Deduct stock
            inv = Inventory.query.filter_by(StoreID=store_id, ProductID=prod_id).first()
            if inv:
                inv.StockQuantity = max(0, inv.StockQuantity - qty)

        new_order.TotalAmount = round(total_amount, 2)
        new_order.TaxAmount = round(total_tax, 2)
        new_order.DiscountAmount = round(total_discount, 2)
        
        # Payment record
        pmt = Payment(
            OrderID=new_order.OrderID,
            PaymentDate=datetime.utcnow(),
            Amount=round(total_amount, 2),
            PaymentMethod=payment_method,
            TransactionStatus='Success',
            TransactionReference=f"TXN-NEW-{new_order.OrderID:06d}"
        )
        db.session.add(pmt)
        
        db.session.commit()
        return jsonify({'success': True, 'order_id': new_order.OrderID, 'message': 'Sales Order Created Successfully!'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
