import hashlib
from crypt import methods

from flask import *
from flask_login import login_required, current_user
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

        user = User.query.filter(User.id == current_user.id).first()
        if check_password_hash(user.password, oldpassword):
            use = User(password=generate_password_hash(newpassword, method='sha256'), username = current_user.username, email = current_user.email)
            db.session.merge(use)
            db.session.commit()
            flash('Password changed successfully.', 'success')
            return redirect(url_for('auth.login'))
        elif oldpassword == newpassword:
            flash('New password should be different from old password', 'danger')
            return redirect(url_for('profile.change_p'))
        else:
            flash('wrong password', 'danger')
            return redirect(url_for('profile.change_p'))
    else:
        flash('Something went wrong', 'danger')
        return 'Something went wrong'

