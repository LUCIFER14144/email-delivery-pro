from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash

from config import config
from models import db, User, Domain, EmailTest
from utils.email_tester import EmailTester
from utils.spam_checker import SpamChecker
from utils.deliverability import DeliverabilityAnalyzer

app = Flask(__name__)
config_name = os.getenv('FLASK_CONFIG') or 'development'
app.config.from_object(config[config_name])
app.secret_key = app.config.get('SECRET_KEY') or 'a_super_secret_key'

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

email_tester = EmailTester()
spam_checker = SpamChecker()
deliverability_analyzer = DeliverabilityAnalyzer()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('landing.html', plans=app.config['PLANS'])

@app.route('/test-db')
def test_db():
    try:
        # Test database connection
        db.session.execute('SELECT 1')
        db.session.commit()
        
        # Test table creation
        db.create_all()
        
        # Try to create a test user
        test_user = User.query.filter_by(email='test@example.com').first()
        if not test_user:
            test_user = User(
                email='test@example.com',
                username='testuser',
                password_hash=generate_password_hash('testpassword')
            )
            db.session.add(test_user)
            db.session.commit()
        
        return {
            'status': 'success',
            'message': 'Database connection successful',
            'details': {
                'database_url': str(app.config['SQLALCHEMY_DATABASE_URI']),
                'tables': [table.name for table in db.get_tables_for_bind()],
                'test_user': {
                    'id': test_user.id,
                    'email': test_user.email,
                    'username': test_user.username
                }
            }
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e),
            'error_type': type(e).__name__,
            'details': {
                'database_url': str(app.config['SQLALCHEMY_DATABASE_URI'])
            }
        }, 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        company_name = request.form.get('company_name', '')
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered')
            return redirect(url_for('login'))
        user = User(email=email, company_name=company_name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    recent_tests = EmailTest.query.filter_by(user_id=current_user.id).order_by(EmailTest.created_at.desc()).limit(5).all()
    total_tests = EmailTest.query.filter_by(user_id=current_user.id).count()
    avg_delivery_rate = db.session.query(db.func.avg(EmailTest.delivery_rate)).filter_by(user_id=current_user.id).scalar() or 0
    avg_spam_score = db.session.query(db.func.avg(EmailTest.spam_score)).filter_by(user_id=current_user.id).scalar() or 0
    domains = Domain.query.filter_by(user_id=current_user.id).all()
    plan_limits = current_user.get_plan_limits()
    tests_this_month = current_user.tests_this_month()
    tests_remaining = plan_limits['max_tests_per_month'] - tests_this_month if plan_limits['max_tests_per_month'] != -1 else 'Unlimited'

    return render_template('dashboard.html',
                           total_tests=total_tests,
                           avg_delivery_rate=round(avg_delivery_rate, 1),
                           avg_spam_score=round(avg_spam_score, 1),
                           recent_tests=recent_tests,
                           domains=domains,
                           plan_limits=plan_limits,
                           tests_this_month=tests_this_month,
                           tests_remaining=tests_remaining)

@app.route('/spam-check')
@login_required
def spam_checker_page():
    return render_template('spam_checker.html')

@app.route('/inbox-test')
@login_required
def inbox_test_page():
    return render_template('inbox_test.html')

def init_db():
    with app.app_context():
        db.create_all()  # This will create all tables
        db.create_all()
        if User.query.count() == 0:
            demo = User(email='demo@example.com', company_name='Demo Company', plan='professional')
            demo.set_password('demo123')
            db.session.add(demo)
            db.session.commit()

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    db.session.rollback()
    return render_template('500.html'), 500

def init_app():
    with app.app_context():
        init_db()
    return app

if __name__ == '__main__':
    init_app()
    app.run(debug=True, host='127.0.0.1', port=5001)

# Vercel serverless function handler
def handler(request, context):
    return init_app()
