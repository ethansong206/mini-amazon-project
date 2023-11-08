from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

from .models.user import User

from flask import Blueprint
bp = Blueprint('users', __name__)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_auth(form.email.data, form.password.data)
        if user is None:
            flash('Invalid email or password')
            return redirect(url_for('users.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index.index')

        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@bp.route('/purchase')
def purchase_history():
    items = User.get_purchase_history(
            uid)
    return jsonify([item.__dict__ for item in items])


class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                       EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        if User.email_exists(email.data):
            raise ValidationError('Already a user with this email.')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.register(form.email.data,
                         form.password.data,
                         form.firstname.data,
                         form.lastname.data):
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))

@bp.route('/info')
def info():
    if current_user.is_authenticated:
        return render_template('info.html', user=User.get(current_user.id))
    else:
        return redirect(url_for('index.index'))

@bp.route('/info/updatefirstname', methods=['POST'])
def update_first():
    id = current_user.id
    firstname = request.form.get('firstname')
    if not firstname == '':
        User.update_firstname(id, firstname)
    return redirect(url_for('users.info'))

@bp.route('/info/updatelastname', methods=['POST'])
def update_last():
    id = current_user.id
    lastname = request.form.get('lastname')
    if not lastname == '':
        User.update_lastname(id, lastname)
    return redirect(url_for('users.info'))

@bp.route('/info/updateaddress', methods=['POST'])
def update_address():
    id = current_user.id
    address = request.form.get('address')
    if not address == '':
        User.update_address(id, address)
    return redirect(url_for('users.info'))

@bp.route('/info/updateemail', methods=['POST'])
def update_email():
    id = current_user.id
    email = request.form.get('email')
    if not email == '':
        User.update_email(id, email)
    return redirect(url_for('users.info'))

@bp.route('/info/updatebalance', methods=['POST'])
def update_balance():
    id = current_user.id
    balance = request.form.get('balance')
    if not balance == '':
        User.update_balance(id, balance)
    return redirect(url_for('users.info'))
    
