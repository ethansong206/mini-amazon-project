from flask import render_template, redirect, url_for
from flask_login import current_user
import datetime
from humanize import naturaltime

from .models.order import Order

from flask import Blueprint
bp = Blueprint('orders', __name__)

def humanize_time(dt):
    return naturaltime(datetime.datetime.now() - dt)

@bp.route('/orders')
def orders():
  if current_user.is_authenticated:
    orders = Order.get_all_by_uid(current_user.id)
    return render_template('order.html', orders=orders, humanize_time=humanize_time)
