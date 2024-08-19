from flask import Blueprint, request, jsonify
from app import db
from models import CustomerAccount

customer_account_bp = Blueprint('customer_account_bp', __name__)

@customer_account_bp.route('/customer_accounts', methods=['POST'])
def create_customer_account():
    data = request.get_json()
    new_account = CustomerAccount(username=data['username'], password=data['password'], customer_id=data['customer_id'])
    db.session.add(new_account)
    db.session.commit()
    return jsonify({'message': 'Customer account created'}), 201

@customer_account_bp.route('/customer_accounts/', methods=['GET'])
def get_customer_account(id):
    account = CustomerAccount.query.get_or_404(id)
    return jsonify({'username': account.username, 'customer_id': account.customer_id})

@customer_account_bp.route('/customer_accounts/', methods=['PUT'])
def update_customer_account(id):
    data = request.get_json()
    account = CustomerAccount.query.get_or_404(id)
    account.username = data['username']
    account.password = data['password']
    db.session.commit()
    return jsonify({'message': 'Customer account updated'})

@customer_account_bp.route('/customer_accounts/', methods=['DELETE'])
def delete_customer_account(id):
    account = CustomerAccount.query.get_or_404(id)
    db.session.delete(account)
    db.session.commit()
    return jsonify({'message': 'Customer account deleted'})