from flask import render_template, redirect, url_for, request
from flask_login import current_user
import datetime
from humanize import naturaltime

from .models.user import User
from .models.inventory import Inventory
from .models.savedproduct import SavedItem
from .models.order import Order

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
        subtotal = SavedItem.get_cart_subtotal(current_user.id)
        user = User.get(current_user.id)
        if subtotal != None:
            return render_template('saved.html',
                                    user=user,   
                                    cart_items=cart_items,
                                    wish_items=wish_items,
                                    subtotal="{:.2f}".format(subtotal),
                                    humanize_time=humanize_time)
        return render_template('saved.html',
                                    cart_items=cart_items,
                                    wish_items=wish_items,
                                    humanize_time=humanize_time)
    return redirect('/')

@bp.route('/saved/checkout', methods=['GET', 'POST'])
def saved_checkout():
    cart_items = SavedItem.get_valid_cart_by_uid(current_user.id)
    subtotal = SavedItem.get_cart_subtotal(current_user.id)
    user = User.get(current_user.id)
    int_balance = int(user.balance)
    return render_template('checkout.html', 
                            cart_items=cart_items, 
                            subtotal="{:.2f}".format(subtotal),
                            int_balance=int_balance,
                            int_subtotal=subtotal,
                            user=user)

@bp.route('/saved/submitorder', methods=['POST'])
def saved_submit_order():
    # where to add check for inventory?

    order_id = SavedItem.submit_order(current_user.id, datetime.datetime.now())
    print('order_id:', order_id)

    if order_id == None:
        return redirect(url_for('saved.saved_order_failed'))
    return redirect(url_for('order.order_get_items', orderid=order_id))

@bp.route('/saved/orderfailed')
def saved_order_failed():
    return render_template('orderfailed.html')

@bp.route('/saved/ordercomplete/<int:orderid>')
def saved_order_complete(orderid):
    order = Order.get(orderid)
    purchases = Order.get_order_items(orderid)
    return render_template('ordercomplete.html',
    order=order,
    purchases=purchases)

@bp.route('/saved/add/<int:pid>', methods=['POST'])
def saved_add(pid):
    SavedItem.add_to_cart(current_user.id, seller_id, pid, 1, datetime.datetime.now())
    return redirect(url_for('saved.saved'))

@bp.route('/saved/update/<int:pid>', methods=['GET', 'POST'])
def saved_updateqty(pid):
    seller_id = request.args.get('sellerid')
    qty = request.form.get('quantity')
    if int(qty) > 0:
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

@bp.route('/saved/remove/<int:pid>', methods=['GET', 'POST'])
def saved_remove(pid):
    seller_id = request.args.get('sellerid')
    SavedItem.remove_item(current_user.id, seller_id, pid)
    return redirect(url_for('saved.saved'))