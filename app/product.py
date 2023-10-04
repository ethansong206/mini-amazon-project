from flask import render_template
from flask_login import current_user
import datetime

from .models.product import Product
from .models.purchase import Purchase

from flask import jsonify

from flask import Blueprint
bp = Blueprint('product', __name__)


@bp.route('/expensive/<varchar(255):category>/<int:k>', methods=['GET'])
def most_expensive(k, category):
    # find the k most expensive products of given category:
    #does not check if category in list, add later
    if k.notnull:
        items = Product.get_most_expensive(k, category)
    else:
        items = None
    # render the page by adding information to the index.html file
    return jsonify([item.__dict__ for item in items])
