from flask import render_template, request, redirect
from flask_login import current_user
import datetime

from .models.product import Product
from .models.savedproduct import SavedItem

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

@bp.route('/product')
def product_page():
    product_id = request.args.get('product_id')

    if product_id is not None:
        product = Product.get(int(product_id))
        sellers = Product.get_all_sellers(int(product_id))
        if product:
            return render_template('product_details.html', product=product, sellers=sellers)
        else:
            return render_template('product_not_found.html')
    return render_template('index.html')
        
@bp.route('/product/addtocart/<int:product_id>', methods = ["POST"])
def product_add_to_cart(product_id):
    print('adding to cart')
    seller_id = request.args.get('seller_id')
    SavedItem.add_to_cart(current_user.id, int(seller_id), int(product_id), 1, datetime.datetime.now())
    return redirect('/saved')