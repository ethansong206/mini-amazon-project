from flask import render_template
from flask_login import current_user

from .models.inventory import Inventory
from .models.seller import Seller

from flask import Blueprint
bp = Blueprint('seller', __name__)

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
