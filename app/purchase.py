from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.purchase import Purchase


from flask import Blueprint
bp = Blueprint('purchase', __name__)

class PurchaseSearchForm(FlaskForm):
    uid = StringField('Purchase user id')
    submit = SubmitField('Search')


@bp.route('/SearchPurchase', methods=['GET', 'POST'])
def purchase():
    form = PurchaseSearchForm()
    # find all purchase for a user:
    uid =form.uid.data
    if uid != '':
        purchases = Purchase.get_all_by_uid(uid)
    else:
        purchases = None
    return render_template('purchase.html',
                            form=form,
                            purchases=purchases)
