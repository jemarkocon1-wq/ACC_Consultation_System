from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from models import db, User, Role, AuditLog, MedicalRecord, HealthRequest
from decorators import role_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
@role_required('Super Admin')
def dashboard():
    total_users = User.query.count()
    total_students = User.query.join(Role).filter(Role.name == 'Student').count()
    total_medical = User.query.join(Role).filter(Role.name == 'Medical Expert').count()
    recent_logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).limit(10).all()

    return render_template('dashboard.html', 
                           role='Super Admin',
                           total_users=total_users,
                           total_students=total_students,
                           total_medical=total_medical,
                           recent_logs=recent_logs)

@admin_bp.route('/users')
@login_required
@role_required('Super Admin')
def manage_users():
    users = User.query.all()
    roles = Role.query.all()
    return render_template('admin_users.html', users=users, roles=roles)

@admin_bp.route('/users/create', methods=['POST'])
@login_required
@role_required('Super Admin')
def create_user():
    username = request.form.get('username')
    email = request.form.get('email')
    full_name = request.form.get('full_name')
    password = request.form.get('password')
    role_id = request.form.get('role_id')

    if User.query.filter((User.username == username) | (User.email == email)).first():
        flash('Username or Email already exists.', 'danger')
        return redirect(url_for('admin.manage_users'))

    new_user = User(
        username=username,
        email=email,
        full_name=full_name,
        password_hash=generate_password_hash(password),
        role_id=role_id,
        is_active=True
    )
    db.session.add(new_user)
    db.session.commit()

    # If student, initialize medical record
    if new_user.role.name == 'Student':
        med_rec = MedicalRecord(student_id=new_user.id)
        db.session.add(med_rec)

    log = AuditLog(user_id=current_user.id, action='Create User', details=f'Created user {username}')
    db.session.add(log)
    db.session.commit()

    flash(f'User {username} created successfully!', 'success')
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/users/toggle/<int:user_id>')
@login_required
@role_required('Super Admin')
def toggle_user_status(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()

    status_str = 'Activated' if user.is_active else 'Deactivated'
    log = AuditLog(user_id=current_user.id, action='Toggle User Status', details=f'{status_str} user {user.username}')
    db.session.add(log)
    db.session.commit()

    flash(f'User {user.username} has been {status_str.lower()}.', 'info')
    return redirect(url_for('admin.manage_users'))
