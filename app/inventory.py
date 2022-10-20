from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.inventory import Inventory


from flask import Blueprint
bp = Blueprint('inventory', __name__)

class InventorySearchForm(FlaskForm):
    uid = StringField('Merchant/Seller ID')
    submit = SubmitField('Search')


@bp.route('/SearchInventory', methods=['GET', 'POST'])
def inventory():
    form = InventorySearchForm()
    uid =form.uid.data
    if uid != '':
        inventory = Inventory.get_all_by_uid(uid)
    else:
        inventory = None
    return render_template('inventory.html',
                            form=form,
                            inventory=inventory)