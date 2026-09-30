from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, User, MedicalRecord, HealthRequest, AuditLog
from decorators import role_required

medical_bp = Blueprint('medical', __name__)

@medical_bp.route('/dashboard')
@login_required
@role_required('Medical Expert')
def dashboard():
    records = MedicalRecord.query.all()
    pending_requests = HealthRequest.query.filter_by(status='Pending').all()
    return render_template('dashboard.html', 
                           role='Medical Expert',
                           records=records, 
                           pending_requests=pending_requests)

@medical_bp.route('/records')
@login_required
@role_required('Medical Expert')
def records():
    records = MedicalRecord.query.all()
    return render_template('medical_records.html', records=records)

@medical_bp.route('/records/update/<int:record_id>', methods=['POST'])
@login_required
@role_required('Medical Expert')
def update_record(record_id):
    rec = MedicalRecord.query.get_or_404(record_id)
    rec.blood_type = request.form.get('blood_type')
    rec.height_cm = request.form.get('height_cm')
    rec.weight_kg = request.form.get('weight_kg')
    rec.allergies = request.form.get('allergies')
    rec.existing_conditions = request.form.get('existing_conditions')
    rec.clearance_status = request.form.get('clearance_status')

    log = AuditLog(user_id=current_user.id, action='Update Medical Record', details=f'Updated medical record for student ID {rec.student_id}')
    db.session.add(log)
    db.session.commit()

    flash('Medical record updated successfully!', 'success')
    return redirect(url_for('medical.records'))

@medical_bp.route('/requests/action/<int:request_id>', methods=['POST'])
@login_required
@role_required('Medical Expert')
def process_request(request_id):
    h_req = HealthRequest.query.get_or_404(request_id)
    action = request.form.get('action') # Approved / Rejected
    notes = request.form.get('notes')

    h_req.status = action
    h_req.doctor_notes = notes

    log = AuditLog(user_id=current_user.id, action='Process Health Request', details=f'{action} request #{h_req.id} for student ID {h_req.student_id}')
    db.session.add(log)
    db.session.commit()

    flash(f'Health Request #{h_req.id} set to {action}.', 'info')
    return redirect(url_for('medical.dashboard'))
