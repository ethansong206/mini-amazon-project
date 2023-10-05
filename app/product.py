from flask import render_template, request
from flask_login import current_user
import datetime

from .models.product import Product

from flask import jsonify

from flask import Blueprint
bp = Blueprint('product', __name__)

@bp.route('/expensive')
def most_expensive():
    k = request.args.get('k')
    if k is not None:
        items = Product.get_most_expensive(int(k))
    else:
        items = None
    return render_template('index.html', avail_products=items)

