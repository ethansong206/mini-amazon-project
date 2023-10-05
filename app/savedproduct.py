from flask import render_template, redirect, url_for
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
    return redirect("/")

@bp.route('/saved/add/<int:pid>', methods=['GET', 'POST'])
def saved_add(pid):
    SavedItem.add_item(current_user.id, pid, 1, True, datetime.datetime.now())
    return redirect(url_for('saved.saved'))

@bp.route('/saved/towishlist/<int:pid>', methods=['GET', 'POST'])
def saved_add_to_wishlist(pid):
    SavedItem.to_wishlist(current_user.id, pid, datetime.datetime.now())
    return redirect(url_for('saved.saved'))

@bp.route('/saved/tocart/<int:pid>', methods=['GET', 'POST'])
def saved_add_to_cart(pid):
    SavedItem.to_cart(current_user.id, pid, datetime.datetime.now())
    return redirect(url_for('saved.saved'))