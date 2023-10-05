from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase
from .models.user import User
from .models.seller import Seller

from flask import Blueprint
bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    is_seller = False
    # get all available products for sale:
    products = Product.get_all(1)
    # find the products current user has bought:
    if current_user.is_authenticated:
        purchases = User.get_purchase_history(current_user.id)
        if Seller.get(current_user.id):
            is_seller = True
    else:
        purchases = None
    # render the page by adding information to the index.html file
    return render_template('index.html',
                           avail_products=products,
                           purchase_history=purchases,
                           is_seller=is_seller)
