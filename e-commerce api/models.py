from database import db

class Customer(db.Model):
    """Model for storing customer details."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=True)
    accounts = db.relationship('CustomerAccount', backref='customer', lazy=True)
    orders = db.relationship('Order', backref='customer', lazy=True)

class CustomerAccount(db.Model):
    """Model for customer accounts."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

class Product(db.Model):
    """Model for products in the catalog."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)

class Order(db.Model):
    """Model for customer orders."""
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    products = db.relationship('Product', secondary='order_product', backref='orders')

class OrderProduct(db.Model):
    """Association table for orders and products."""
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
