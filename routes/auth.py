from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from models import db, User, AuditLog

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect_dashboard(current_user.role.name)

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            if not user.is_active:
                flash('Your account has been deactivated. Contact Super Admin.', 'danger')
                return render_template('login.html')

            login_user(user)
            log = AuditLog(user_id=user.id, action='User Login', details=f'{user.username} logged in successfully.')
            db.session.add(log)
            db.session.commit()

            return redirect_dashboard(user.role.name)
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    log = AuditLog(user_id=current_user.id, action='User Logout', details=f'{current_user.username} logged out.')
    db.session.add(log)
    db.session.commit()
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('auth.login'))

def redirect_dashboard(role_name):
    if role_name == 'Super Admin':
        return redirect(url_for('admin.dashboard'))
    elif role_name == 'Medical Expert':
        return redirect(url_for('medical.dashboard'))
    elif role_name == 'Student':
        return redirect(url_for('student.dashboard'))
    return redirect(url_for('auth.login'))
