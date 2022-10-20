from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.review import Review


from flask import Blueprint
bp = Blueprint('review', __name__)

class ReviewSearchForm(FlaskForm):
    uid = StringField('Purchase user id')
    submit = SubmitField('Search')


@bp.route('/SearchReview', methods=['GET', 'POST'])
def review():
    form = ReviewSearchForm()
    # find all purchase for a user:
    uid =form.uid.data
    if uid != '':
        reviews = Review.get_all_by_uid_recent(uid)
    else:
        reviews = None
    return render_template('review.html',
                            form=form,
                            reviews=reviews)
