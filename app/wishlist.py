from flask import render_template
from flask_login import current_user
import datetime

from .models.wishlist import WishlistItem
from .models.product import Product
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('wishlist', __name__)

from flask import jsonify
from flask import redirect, url_for

@bp.route('/wishlist')
def wishlist():
    # find the products current user has in wishlist:
    if current_user.is_authenticated:
        items = WishlistItem.get_all_by_uid_since(
            current_user.id, datetime.datetime(1980, 9, 14, 0, 0, 0))
    else:
        return jsonify({}), 404
    # render the page by adding information to the wishlist.html file
    return jsonify([item.__dict__ for item in items])

@bp.route('/wishlist/add/<int:product_id>', methods=['POST'])
def wishlist_add(product_id):
    #add an item into wishlist
    WishlistItem.wishlist_add(current_user.id, product_id, datetime.datetime.now())
    return redirect(url_for('wishlist.wishlist'))
