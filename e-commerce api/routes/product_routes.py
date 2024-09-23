from flask import request, jsonify
from models import Product
from database import db
from . import product_bp

@product_bp.route('/products', methods=['POST'])
def create_product():
    """Create a new product."""
    data = request.json
    if 'name' not in data or 'price' not in data:
        return jsonify({"error": "Name and price are required."}), 400

    try:
        new_product = Product(name=data['name'], price=data['price'], stock=data.get('stock', 0))
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"id": new_product.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@product_bp.route('/products/<int:id>', methods=['GET'])
def read_product(id):
    """Retrieve a product by ID."""
    product = Product.query.get_or_404(id)
    return jsonify({"id": product.id, "name": product.name, "price": product.price, "stock": product.stock})

@product_bp.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    """Update product details."""
    data = request.json
    product = Product.query.get_or_404(id)
    
    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    product.stock = data.get('stock', product.stock)
    
    db.session.commit()
    return jsonify({"message": "Product updated"})

@product_bp.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    """Delete a product by ID."""
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"})

@product_bp.route('/products', methods=['GET'])
def list_products():
    """List all products."""
    products = Product.query.all()
    return jsonify([{"id": p.id, "name": p.name, "price": p.price, "stock": p.stock} for p in products])

@product_bp.route('/products/<int:id>/stock', methods=['PUT'])
def update_product_stock(id):
    """Update product stock levels."""
    data = request.json
    product = Product.query.get_or_404(id)

    if 'stock' not in data:
        return jsonify({"error": "Stock level is required."}), 400

    product.stock = data['stock']
    db.session.commit()
    return jsonify({"message": "Product stock updated"})
