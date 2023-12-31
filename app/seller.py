from flask import render_template, request, redirect, url_for
from humanize import naturaltime
from datetime import datetime
from flask_login import current_user

from .models.inventory import Inventory
from .models.seller import Seller

from flask import Blueprint
bp = Blueprint('seller', __name__)

def humanize_time(dt):
    return naturaltime(datetime.now() - dt)

@bp.route('/seller')
def seller():
    if current_user.is_authenticated:
        is_seller = False
        inventory_items = []
        if Seller.get(current_user.id):
            is_seller = True
            inventory_items = Inventory.get_all_from_seller(current_user.id)
        return render_template('seller.html',
                                is_seller = is_seller,
                                inventory_items = inventory_items)
    return None

@bp.route('/seller/orders')
def seller_get_orders():
    if current_user.is_authenticated and Seller.get(current_user.id):
        order_items = Seller.get_orders(current_user.id)
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        return render_template('sellerorders.html',
                                order_items = order_items,
                                humanize_time = humanize_time,
                                datetime = datetime,
                                months = months)

    return redirect('/')

@bp.route('/seller/update-qty', methods=['POST'])
def update_inventory_qty():
    pid = request.args.get('pid')
    qty = request.form.get('quantity')
    if int(qty) > 0:
        Inventory.update_inventory_qty(pid, current_user.id, qty)
    return redirect(url_for('seller.seller'))

@bp.route('/seller/update-price', methods=['POST'])
def update_inventory_price():
    pid = request.args.get('pid')
    price = request.form.get('price')
    if float(price) > 0:
        Inventory.update_inventory_price(pid, current_user.id, price)
    return redirect(url_for('seller.seller'))
