from flask import render_template
from flask_login import current_user
from humanize import naturaltime
import datetime

from .models.product import Product
from .models.purchase import Purchase
from .models.savedproduct import SavedItem
from .models.user import User
from .models.seller import Seller

from flask import Blueprint
bp = Blueprint('index', __name__)

def humanize_time(dt):
    return naturaltime(datetime.datetime.now() - dt)

@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/index')
def index():
    is_seller = False
    # get all available products for sale:
    products = Product.get_all(1)
    cart = []
    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = User.get_purchase_history(current_user.id)
        if Seller.get(current_user.id):
            is_seller = True
        cart = SavedItem.get_valid_cart_by_uid(current_user.id)
    else:
        purchases = None
    # render the page by adding information to the index.html file
    categories = Product.get_all_categories()
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    return render_template('index.html',
                           avail_products=products,
                           purchase_history=purchases,
                           is_seller=is_seller,
                           categories=categories,
                           months=months,
                           humanize_time=humanize_time,
                           cart=cart)
