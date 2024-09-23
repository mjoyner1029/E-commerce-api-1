from flask import request, jsonify
from models import Order, Product
from database import db
from datetime import datetime
from . import order_bp

@order_bp.route('/orders', methods=['POST'])
def place_order():
    """Place a new order."""
    data = request.json
    if 'customer_id' not in data or 'products' not in data:
        return jsonify({"error": "Customer ID and products are required."}), 400

    try:
        new_order = Order(order_date=datetime.utcnow(), customer_id=data['customer_id'])
        db.session.add(new_order)
        for product_id in data['products']:
            product = Product.query.get_or_404(product_id)
            new_order.products.append(product)
        db.session.commit()
        return jsonify({"id": new_order.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@order_bp.route('/orders/<int:id>', methods=['GET'])
def retrieve_order(id):
    """Retrieve an order by ID."""
    order = Order.query.get_or_404(id)
    products = [{"id": p.id} for p in order.products]
    return jsonify({"id": order.id, "order_date": order.order_date, "customer_id": order.customer_id, "products": products})

@order_bp.route('/orders', methods=['GET'])
def list_orders():
    """List all orders."""
    orders = Order.query.all()
    return jsonify([{"id": o.id, "order_date": o.order_date, "customer_id": o.customer_id} for o in orders])

@order_bp.route('/orders/<int:id>', methods=['DELETE'])
def cancel_order(id):
    """Cancel an order by ID."""
    order = Order.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": "Order canceled"})
