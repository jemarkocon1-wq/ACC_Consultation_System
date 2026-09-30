import os
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash

from models import db, User, Role, MedicalRecord, HealthRequest, AuditLog
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.medical import medical_bp
from routes.student import student_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'abuyog-community-college-mlbb-super-secret-key-2026'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///abuyog_health.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(medical_bp, url_prefix='/medical')
    app.register_blueprint(student_bp, url_prefix='/student')

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    # Seed initial data
    with app.app_context():
        db.create_all()
        seed_initial_data()

    return app

def seed_initial_data():
    if not Role.query.first():
        admin_role = Role(name='Super Admin', description='Full System Controller')
        med_role = Role(name='Medical Expert', description='Health & Clinic Administrator')
        student_role = Role(name='Student', description='ACC Student User')

        db.session.add_all([admin_role, med_role, student_role])
        db.session.commit()

        # Seed Users
        admin_user = User(
            username='admin',
            email='admin@abuyog.edu.ph',
            password_hash=generate_password_hash('admin123'),
            full_name='Mythic Super Admin',
            role_id=admin_role.id,
            is_active=True
        )

        med_user = User(
            username='doc_smith',
            email='dr.smith@abuyog.edu.ph',
            password_hash=generate_password_hash('doc123'),
            full_name='Dr. Lesley Vance, MD',
            role_id=med_role.id,
            is_active=True
        )

        student_user = User(
            username='student1',
            email='ling.2024@abuyog.edu.ph',
            password_hash=generate_password_hash('student123'),
            full_name='Ling Nightshade',
            role_id=student_role.id,
            is_active=True
        )

        db.session.add_all([admin_user, med_user, student_user])
        db.session.commit()

        # Seed sample record
        record = MedicalRecord(
            student_id=student_user.id,
            blood_type='O+',
            height_cm=175.5,
            weight_kg=68.0,
            allergies='Penicillin, Dust',
            existing_conditions='Mild Asthma',
            clearance_status='Cleared'
        )
        db.session.add(record)

        # Seed sample log
        log = AuditLog(
            user_id=admin_user.id,
            action='System Initialization',
            details='Initial seed data created for Abuyog Community College Health System.'
        )
        db.session.add(log)
        db.session.commit()

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
