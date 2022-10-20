from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.cart import Cart


from flask import Blueprint
bp = Blueprint('cart', __name__)

class CartSearchForm(FlaskForm):
    uid = StringField('Purchase user id')
    submit = SubmitField('Search')


@bp.route('/SearchCart', methods=['GET', 'POST'])
def cart():
    form = CartSearchForm()
    # find all purchase for a user:
    uid =form.uid.data
    if uid != '':
        cart_item = Cart.get_all_by_uid(uid)
    else:
        cart_item  = None
    return render_template('cart.html',
                            form=form,
                            cart=cart_item)
