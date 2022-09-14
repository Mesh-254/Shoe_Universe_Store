import mail
from flask import *
from flask_login import login_user, logout_user, current_user
from random_password import random_password

from models.user import User
from werkzeug.security import check_password_hash, generate_password_hash
from models.database import db
from flask_mail import Message

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    """login method"""
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    """login method"""
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(username=username).first()
    if not user:
        flash('You are not registered. Please signup now.', 'danger')
        return redirect(url_for('auth.signup_post'))
    elif not check_password_hash(user.password, password):
        flash('Please check your login details and try again.', 'danger')
        return redirect(url_for('auth.login'))
    else:
        login_user(user, remember=remember)
        flash('You have successfully logged in', 'success')
        return redirect(url_for('index'))


@auth.route('/signup')
def signup():
    """signup method"""
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    """signup method"""
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if password != confirm_password:
        flash('passwords do not match!', category='danger')
        return redirect(url_for('auth.signup'))

    if len(password) < 4 or len(confirm_password) < 4:
        flash('Passwords must be at least 4 characters.', category='danger')
        return redirect(url_for('auth.signup'))

    user = User.query.filter_by(email=email).first()
    userName = User.query.filter_by(username=username).first()
    new_user = User(username=username, email=email, password=generate_password_hash(password, method='sha256'))
    if user or userName:
        flash('You are already registered', 'danger')
        return redirect(url_for('auth.login'))
    else:
        db.session.add(new_user)
        db.session.commit()
        flash('You have been registered!', category='success')
        return redirect(url_for('auth.login'))


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/reset_password')
def reset_password():
    return render_template('reset_password.html')


@auth.route('/reset_password', methods=['POST'])
def reset_password_post():
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if not user:
        flash('User email does not exist', 'danger')
        return redirect(url_for('auth.reset_password'))
    else:
        send_password_reset_email(user)
    token = random_password()
    user.password = generate_password_hash(token, method='sha256')
    db.session.commit()

    msg = Message('Password Reset Request',
                  sender='info@shoe_store.com',
                  recipients=[user.email])
    msg.body = f'To reset your password, Use this temporary token: {token}'
    mail.send(msg)
    flash('An email has been sent with instructions to reset your password', 'success')
    return redirect(url_for('auth.login'))
