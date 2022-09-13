import hashlib
from crypt import methods

from flask import *
from flask_login import login_required, current_user

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
def change_p():
    return render_template('changepassword.html')


@profile.route('/account/profile/changePassword', methods=['GET', 'POST'])
@login_required
def change_password():
    """change password"""
    if request.method == 'POST':
        oldpassword = request.form.get('oldpassword')
        newpassword = request.form.get('newpassword')

        password = User.query.get('password').filter_by(username=current_user.username).first()
        if password == oldpassword:
            try:
                password = User(password=newpassword)
                flash('Password changed successfully.', 'success')
            except:
                flash('Failed to change password', 'danger')
            return redirect(url_for('/'))
        elif oldpassword == newpassword:
            flash('New password should be different from old password', 'danger')
        else:
            flash('wrong password', 'danger')
        return redirect(url_for('profile.change_p'))
    else:
        return 'Something went wrong'
        flash('Something went wrong', 'danger')
