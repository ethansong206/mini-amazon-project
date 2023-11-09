from flask import render_template, request, redirect, url_for
from flask_login import current_user
import datetime

from .models.product import Product
from .models.order import Order
from .models.savedproduct import SavedItem

from flask import jsonify

from flask import Blueprint
bp = Blueprint('product', __name__)

@bp.route('/expensive')
def most_expensive():
    k = request.args.get('k')
    categories = Product.get_all_categories()
    if k is not None:
        items = Product.get_most_expensive(int(k))
    else:
        items = None
    return render_template('index.html', avail_products=items, categories=categories)

@bp.route('/filter')
def all_category():
    category = request.args.get('category')
    categories = Product.get_all_categories()
    if category != "":
        items = Product.get_all_from_category(category)
    else:
        items = Product.get_all(1)
    return render_template('index.html', avail_products=items, category=category, categories=categories)

@bp.route('/search')
def search_for():
    categories = Product.get_all_categories()
    text = request.args.get('search')
    items = Product.search(text)
    return render_template('index.html', avail_products=items, categories=categories)

@bp.route('/product')
def product_page():
    product_id = request.args.get('product_id')

    if product_id is not None:
        product = Product.get(int(product_id))
        sellers = Product.get_all_sellers(current_user.id, int(product_id))

        if product:
            return render_template('product_details.html', 
                                    product=product, 
                                    sellers=sellers)
        else:
            return render_template('product_not_found.html')
    return render_template('index.html')
        
@bp.route('/product/addtocart/<int:product_id>', methods = ["POST"])
def product_add_to_cart(product_id):
    print('adding to cart')
    seller_id = request.args.get('seller_id')
    num_items = request.form.get('quantity')
    if int(num_items) > 0:
        SavedItem.add_to_cart(current_user.id, int(seller_id), int(product_id), num_items, datetime.datetime.now())
        return redirect('/saved')
    else:
        return redirect(url_for('product.product_page', product_id=product_id))

@bp.route('/product/<int:orderid>', methods=['GET'])
def product_get_items(orderid):
  if current_user.is_authenticated:
    order_items = Order.get_order_items(orderid)
    return render_template('orderitems.html',
    order_items=order_items,
    order_id=orderid,
    humanize_time=humanize_time)