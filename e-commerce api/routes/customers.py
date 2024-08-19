from flask import Blueprint, request, jsonify
from app import db
from models import Customer

customer_bp = Blueprint('customer_bp', __name__)

@customer_bp.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    new_customer = Customer(name=data['name'], email=data['email'], phone=data['phone'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer created'}), 201

@customer_bp.route('/customers/', methods=['GET'])
def get_customer(id):
    customer = Customer.query.get_or_404(id)
    return jsonify({'name': customer.name, 'email': customer.email, 'phone': customer.phone})

@customer_bp.route('/customers/', methods=['PUT'])
def update_customer(id):
    data = request.get_json()
    customer = Customer.query.get_or_404(id)
    customer.name = data['name']
    customer.email = data['email']
    customer.phone = data['phone']
    db.session.commit()
    return jsonify({'message': 'Customer updated'})

@customer_bp.route('/customers/', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted'})