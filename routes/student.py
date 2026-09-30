from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, MedicalRecord, HealthRequest, AuditLog
from decorators import role_required

student_bp = Blueprint('student', __name__)

@student_bp.route('/dashboard')
@login_required
@role_required('Student')
def dashboard():
    record = MedicalRecord.query.filter_by(student_id=current_user.id).first()
    my_requests = HealthRequest.query.filter_by(student_id=current_user.id).order_by(HealthRequest.submitted_at.desc()).all()
    return render_template('dashboard.html', 
                           role='Student',
                           record=record, 
                           my_requests=my_requests)

@student_bp.route('/request/submit', methods=['GET', 'POST'])
@login_required
@role_required('Student')
def submit_request():
    if request.method == 'POST':
        request_type = request.form.get('request_type')
        reason = request.form.get('reason')

        new_req = HealthRequest(
            student_id=current_user.id,
            request_type=request_type,
            reason=reason,
            status='Pending'
        )
        db.session.add(new_req)

        log = AuditLog(user_id=current_user.id, action='Submit Health Request', details=f'Submitted request: {request_type}')
        db.session.add(log)
        db.session.commit()

        flash('Your health request has been submitted to the clinic.', 'success')
        return redirect(url_for('student.dashboard'))

    return render_template('health_request.html')
