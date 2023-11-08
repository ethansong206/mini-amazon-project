from flask import render_template, redirect, url_for, request
from flask_login import current_user
import datetime
from humanize import naturaltime

from .models.savedproduct import SavedItem

from flask import Blueprint
bp = Blueprint('saved', __name__)

# EVERYTHING HAS TO BE UPDATED SO THAT WE USE THE THREE KEYS TO UPDATE SAVED ITEMS

def humanize_time(dt):
    return naturaltime(datetime.datetime.now() - dt)

@bp.route('/saved')
def saved():
    if current_user.is_authenticated:
        cart_items = SavedItem.get_all_cart_by_uid(current_user.id)
        wish_items = SavedItem.get_all_wishlist_by_uid(current_user.id)
        return render_template('saved.html',
                                cart_items=cart_items,
                                wish_items=wish_items,
                                humanize_time=humanize_time)
    return redirect('/')

@bp.route('/saved/add/<int:pid>', methods=['POST'])
def saved_add(pid):
    SavedItem.add_to_cart(current_user.id, seller_id, pid, 1, datetime.datetime.now())
    return redirect(url_for('saved.saved'))

@bp.route('/saved/update/<int:pid>', methods=['GET', 'POST'])
def saved_updateqty(pid):
    seller_id = request.args.get('sellerid')
    qty = request.form.get('quantity')
    SavedItem.update_quantity(current_user.id, seller_id, pid, qty)
    return redirect(url_for('saved.saved'))

@bp.route('/saved/towishlist/<int:pid>', methods=['GET', 'POST'])
def saved_to_wishlist(pid):
    seller_id = request.args.get('sellerid')
    SavedItem.move_to_wishlist(current_user.id, seller_id, pid, datetime.datetime.now())
    return redirect(url_for('saved.saved'))

@bp.route('/saved/tocart/<int:pid>', methods=['GET', 'POST'])
def saved_to_cart(pid):
    seller_id = request.args.get('sellerid')
    SavedItem.move_to_cart(current_user.id, seller_id, pid, datetime.datetime.now())
    return redirect(url_for('saved.saved'))