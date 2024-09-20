from flask import Blueprint

customer_bp = Blueprint('customers', __name__)
product_bp = Blueprint('products', __name__)
order_bp = Blueprint('orders', __name__)

from .customer_routes import *
from .product_routes import *
from .order_routes import *
