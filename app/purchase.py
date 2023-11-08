from flask import render_template, redirect, url_for
from flask_login import current_user
import datetime
from humanize import naturaltime

from .models.order import Order
from .models.purchase import Purchase

from flask import Blueprint
bp = Blueprint('order', __name__)

def humanize_time(dt):
  return naturaltime(datetime.datetime.now() - dt)

@bp.route('/order/<int:orderid>', methods=['GET'])
def order_get_items(orderid):
  if current_user.is_authenticated:
    order_items = Order.get_order_items(orderid)
    return render_template('orderitems.html',
    order_items=order_items,
    order_id=orderid,
    humanize_time=humanize_time)