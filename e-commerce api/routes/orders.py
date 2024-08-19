from flask import Blueprint, request, jsonify
from app import db
from models import Order, OrderProduct, Product

order_bp = Blueprint('order_bp', __name__)

@order_bp.route('/orders', methods=['POST'])
def place_order():
    data = request.get_json()
    new_order = Order(customer_id=data['customer_id'])
    db.session.add(new_order)
    db.session.commit()

    for product in data['products']:
        order_product = OrderProduct(order_id=new_order.id, product_id=product['product_id'], quantity=product['quantity'])
        db.session.add(order_product)
    
    db.session.commit()
    return jsonify({'message': 'Order placed'}), 201

@order_bp.route('/orders/', methods=['GET'])
def retrieve_order(id):
    order = Order.query.get_or_404(id)
    order_products = OrderProduct.query.filter_by(order_id=id).all()
    products = [{'product_id': op.product_id, 'quantity': op.quantity} for op in order_products]
    return jsonify({'customer_id': order.customer_id, 'order_date': order.order_date, 'status': order.status, 'products': products})

@order_bp.route('/orders/', methods=['PUT'])
def update_order(id):
    data = request.get_json()
    order = Order.query.get_or_404(id)
    order.status = data['status']
    db.session.commit()
    return jsonify({'message': 'Order updated'})

@order_bp.route('/orders/', methods=['DELETE'])
def delete_order(id):
    order = Order.query.get_or_404(id)