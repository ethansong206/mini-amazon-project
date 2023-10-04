from flask import render_template
from flask_login import current_user
import datetime

from .models.savedproduct import SavedItem

from flask import Blueprint
bp = Blueprint('saved', __name__)

@bp.route('/saved')
def saved():
    if current_user.is_authenticated:
        cart_items = SavedItem.get_all_cart_by_uid(current_user.id)
        wish_items = SavedItem.get_all_wishlist_by_uid(current_user.id)
        return render_template('saved.html',
                                cart_items=cart_items,
                                wish_items=wish_items)
    return None