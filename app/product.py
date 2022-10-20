from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.product import Product


from flask import Blueprint
bp = Blueprint('product', __name__)

class ProductSearchForm(FlaskForm):
    k = StringField('Price Rank Top k')
    submit = SubmitField('Search')


@bp.route('/SearchProduct', methods=['GET', 'POST'])
def product():
    form = ProductSearchForm()
    k =form.k.data
    if k != '':
        products = Product.get_by_top_k(k)
    else:
        products = None
    return render_template('product.html',
                            form=form,
                            products=products)