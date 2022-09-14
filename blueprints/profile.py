import hashlib
from crypt import methods

from flask import *
from flask_login import login_required, current_user, fresh_login_required
from werkzeug.security import generate_password_hash, check_password_hash

from models.user import User
from models.database import db

profile = Blueprint('profile', __name__)


@profile.route('/account/profile')
def account_profile():
    return render_template('profile.html')


@profile.route('/account/profile/edit')
@login_required
def account_profile_edit():
    """edit profile"""
    return render_template('editProfile.html')


@profile.route('/account/profile/update', methods=['GET', 'POST'])
@login_required
def account_profile_update():
    """update profile"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        try:
            new_user = User(username=username, email=email)
            db.session.add(new_user)
            db.session.commit()
            flash('Profile updated successfully', 'success')
        except:
            db.session.rollback()
            flash('Profile update failed!', 'danger')
        return redirect(url_for('profile.account_profile'))


@profile.route('/account/profile/change', methods=['GET', 'POST'])
@login_required
def change_p():
    return render_template('changepassword.html')


@profile.route('/account/profile/changePassword', methods=['GET', 'POST'])
@login_required
def change_password():
    """change password"""
    if request.method == 'POST':
        oldpassword = request.form.get('oldpassword')
        newpassword = request.form.get('newpassword')
        newpassword1 = request.form.get('newpassword1')

        user = User.query.filter(User.id == current_user.id).first()
        if oldpassword == newpassword:
            flash('New password should be different from previous password', 'danger')
            return redirect(url_for('profile.change_p'))
        if len(newpassword) < 4 or len(newpassword1) < 4:
            flash('Passwords must be at least 4 characters.', category='danger')
            return redirect(url_for('profile.change_p'))
        if newpassword != newpassword1:
            flash('Your new passwords do not match!', category='danger')
            return redirect(url_for('profile.change_p'))
        if check_password_hash(user.password, oldpassword):
            User.password = generate_password_hash(newpassword, method='sha256')
            db.session.commit()
            flash('Password changed successfully.', 'success')
            return redirect(url_for('auth.logout'))
            return redirect(url_for('auth.login'))
        else:
            flash('wrong password', 'danger')
            return redirect(url_for('profile.change_p'))
    else:
        flash('Something went wrong', 'danger')
        return 'Something went wrong'


@profile.route('/wishlist', methods=['GET', 'POST'])
def wishlist():
    """ Wish list method """
    return render_template('add-to-wishlist.html')
