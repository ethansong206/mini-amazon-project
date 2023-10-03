from flask import render_template
from flask_login import current_user
import datetime

from .models.wishlist import WishlistItem

from flask import Blueprint
bp = Blueprint('wishlist', __name__)

from flask import jsonify

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