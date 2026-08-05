from flask import Blueprint, render_template, request, jsonify
from sqlalchemy import text
from models import db, Product, Category, Supplier, Inventory, Store

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/')
def inventory_dashboard():
    store_id = request.args.get('store_id', None, type=int)
    category_id = request.args.get('category_id', None, type=int)
    low_stock_only = request.args.get('low_stock', 0, type=int)

    sql = """
    SELECT 
        i.InventoryID,
        st.StoreName,
        st.Region,
        p.ProductID,
        p.SKU,
        p.ProductName,
        c.CategoryName,
        i.StockQuantity,
        i.ReorderLevel,
        p.CostPrice,
        p.SellingPrice,
        (i.StockQuantity * p.CostPrice) AS InventoryCostValue,
        CASE 
            WHEN i.StockQuantity = 0 THEN 'Out of Stock'
            WHEN i.StockQuantity <= i.ReorderLevel THEN 'Low Stock'
            ELSE 'In Stock'
        END AS StockStatus
    FROM Inventory i
    JOIN Stores st ON i.StoreID = st.StoreID
    JOIN Products p ON i.ProductID = p.ProductID
    JOIN Categories c ON p.CategoryID = c.CategoryID
    WHERE 1=1
    """
    params = {}
    if store_id:
        sql += " AND i.StoreID = :store_id"
        params['store_id'] = store_id
    if category_id:
        sql += " AND p.CategoryID = :category_id"
        params['category_id'] = category_id
    if low_stock_only:
        sql += " AND i.StockQuantity <= i.ReorderLevel"

    sql += " ORDER BY i.StockQuantity ASC LIMIT 200"

    items = db.session.execute(text(sql), params).fetchall()

    stores = Store.query.all()
    categories = Category.query.all()

    return render_template('inventory.html', 
                           items=items, 
                           stores=stores, 
                           categories=categories,
                           current_store=store_id,
                           current_category=category_id,
                           low_stock_only=low_stock_only)
