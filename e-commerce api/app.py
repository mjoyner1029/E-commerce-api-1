from flask import Flask
from database import db, app
from routes import customer_bp, product_bp, order_bp

# Register Blueprints
app.register_blueprint(customer_bp, url_prefix='/api')
app.register_blueprint(product_bp, url_prefix='/api')
app.register_blueprint(order_bp, url_prefix='/api')

# Create database tables
with app.app_context():
    db.drop_all()  # Clear existing tables
    db.create_all()  # Create new tables

if __name__ == '__main__':
    app.run(debug=True)
