from flask import render_template
from flask import jsonify
from flask import redirect, url_for
from flask_login import current_user
from humanize import naturaltime
import datetime

def humanize_time(dt):
    return naturaltime(datetime.datetime.now() - dt)

from .models.wishlist import WishlistItem

from flask import Blueprint
bp = Blueprint('wishlist', __name__)

@bp.route('/wishlist')
def wishlist():
    if not current_user.is_authenticated:
        return jsonify({}), 404

    items = WishlistItem.get_all_by_uid(current_user.id)
    return render_template('wishlist.html',
                      items=items,
                      humanize_time=humanize_time)

@bp.route('/wishlist/add/<int:product_id>', methods=['POST'])
def wishlist_add(product_id):
    WishlistItem.add(current_user.id, product_id, datetime.datetime.now())
    return redirect(url_for('wishlist.wishlist'))
