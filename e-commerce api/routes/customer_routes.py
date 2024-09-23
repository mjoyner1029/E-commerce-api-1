from flask import request, jsonify
from models import Customer, CustomerAccount
from database import db
from . import customer_bp

@customer_bp.route('/customers', methods=['POST'])
def create_customer():
    """Create a new customer."""
    data = request.json
    if not all(key in data for key in ('name', 'email')):
        return jsonify({"error": "Name and email are required."}), 400

    try:
        new_customer = Customer(name=data['name'], email=data['email'], phone=data.get('phone'))
        db.session.add(new_customer)
        db.session.commit()
        return jsonify({"id": new_customer.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@customer_bp.route('/customers/<int:id>', methods=['GET'])
def read_customer(id):
    """Retrieve a customer by ID."""
    customer = Customer.query.get_or_404(id)
    return jsonify({"id": customer.id, "name": customer.name, "email": customer.email, "phone": customer.phone})

@customer_bp.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    """Update customer details."""
    data = request.json
    customer = Customer.query.get_or_404(id)
    
    customer.name = data.get('name', customer.name)
    customer.email = data.get('email', customer.email)
    customer.phone = data.get('phone', customer.phone)
    
    db.session.commit()
    return jsonify({"message": "Customer updated"})

@customer_bp.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    """Delete a customer by ID."""
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer deleted"})

@customer_bp.route('/customer_accounts', methods=['POST'])
def create_customer_account():
    """Create a new customer account."""
    data = request.json
    if 'username' not in data or 'password' not in data or 'customer_id' not in data:
        return jsonify({"error": "Username, password, and customer ID are required."}), 400

    try:
        new_account = CustomerAccount(username=data['username'], password=data['password'], customer_id=data['customer_id'])
        db.session.add(new_account)
        db.session.commit()
        return jsonify({"id": new_account.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Implement Read, Update, and Delete for CustomerAccount...
