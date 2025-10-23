# 8. Create app.py - Main Flask application
app_content = '''from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta
import json
import os

# Import our custom modules
from config import config
from models import db, User, Domain, EmailTest
from utils.email_tester import EmailTester
from utils.spam_checker import SpamChecker
from utils.deliverability import DeliverabilityAnalyzer

# Initialize Flask app
app = Flask(__name__)

# Configure app
config_name = os.getenv('FLASK_CONFIG') or 'development'
app.config.from_object(config[config_name])

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize utility classes
email_tester = EmailTester()
spam_checker = SpamChecker()
deliverability_analyzer = DeliverabilityAnalyzer()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    """Landing page"""
    return render_template('landing.html', 
                         plans=app.config['PLANS'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        company_name = request.form.get('company_name', '')
        
        # Check if user exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered')
            return redirect(url_for('login'))
        
        # Create new user
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
    """User logout"""
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard"""
    # Get user's recent tests
    recent_tests = EmailTest.query.filter_by(user_id=current_user.id)\\
                                  .order_by(EmailTest.created_at.desc())\\
                                  .limit(5).all()
    
    # Calculate summary stats
    total_tests = EmailTest.query.filter_by(user_id=current_user.id).count()
    
    if total_tests > 0:
        avg_delivery_rate = db.session.query(db.func.avg(EmailTest.delivery_rate))\\
                                     .filter_by(user_id=current_user.id).scalar() or 0
        avg_spam_score = db.session.query(db.func.avg(EmailTest.spam_score))\\
                                  .filter_by(user_id=current_user.id).scalar() or 0
    else:
        avg_delivery_rate = 0
        avg_spam_score = 0
    
    # Get user domains
    domains = Domain.query.filter_by(user_id=current_user.id).all()
    
    # Get plan limits
    plan_limits = current_user.get_plan_limits()
    tests_this_month = current_user.tests_this_month()
    
    dashboard_data = {
        'total_tests': total_tests,
        'avg_delivery_rate': round(avg_delivery_rate, 1),
        'avg_spam_score': round(avg_spam_score, 1),
        'recent_tests': recent_tests,
        'domains': domains,
        'plan_limits': plan_limits,
        'tests_this_month': tests_this_month,
        'tests_remaining': plan_limits['max_tests_per_month'] - tests_this_month if plan_limits['max_tests_per_month'] != -1 else 'Unlimited'
    }
    
    return render_template('dashboard.html', **dashboard_data)

@app.route('/spam-checker', methods=['GET', 'POST'])
@login_required
def spam_checker_route():
    """Spam score checker tool"""
    if request.method == 'POST':
        # Check rate limits
        if not check_rate_limit():
            flash('Rate limit exceeded. Please try again later.')
            return redirect(url_for('spam_checker_route'))
        
        # Get form data
        subject = request.form['subject']
        sender_email = request.form['sender_email']
        html_content = request.form['html_content']
        text_content = request.form.get('text_content', '')
        
        # Analyze email
        test_results = email_tester.analyze_email(subject, sender_email, html_content, text_content)
        spam_results = spam_checker.check_content(subject, html_content, text_content)
        
        # Save test to database
        email_test = EmailTest(
            user_id=current_user.id,
            subject=subject,
            sender_email=sender_email,
            html_content=html_content,
            text_content=text_content,
            overall_score=test_results['overall_score'],
            spam_score=spam_results['spam_score'],
            delivery_rate=test_results['delivery_rate'],
            status='completed',
            completed_at=datetime.utcnow()
        )
        
        email_test.set_provider_results(test_results['provider_results'])
        email_test.set_spam_factors(test_results['spam_factors'])
        
        db.session.add(email_test)
        db.session.commit()
        
        return render_template('spam_checker_results.html', 
                             test_results=test_results,
                             spam_results=spam_results,
                             test_id=email_test.id)
    
    return render_template('spam_checker.html')

@app.route('/inbox-test', methods=['GET', 'POST'])
@login_required  
def inbox_test():
    """Inbox placement testing tool"""
    if request.method == 'POST':
        # Check rate limits
        if not check_rate_limit():
            flash('Rate limit exceeded. Please try again later.')
            return redirect(url_for('inbox_test'))
        
        # Get form data
        subject = request.form['subject']
        sender_email = request.form['sender_email']
        html_content = request.form['html_content']
        
        # Run comprehensive analysis
        test_results = email_tester.analyze_email(subject, sender_email, html_content)
        
        # Get domain for additional analysis
        domain = sender_email.split('@')[1] if '@' in sender_email else None
        domain_health = None
        
        if domain:
            domain_health = deliverability_analyzer.analyze_domain_health(domain)
        
        # Save test
        email_test = EmailTest(
            user_id=current_user.id,
            subject=subject,
            sender_email=sender_email,
            html_content=html_content,
            overall_score=test_results['overall_score'],
            spam_score=test_results['spam_score'],
            delivery_rate=test_results['delivery_rate'],
            test_type='inbox_placement',
            status='completed',
            completed_at=datetime.utcnow()
        )
        
        email_test.set_provider_results(test_results['provider_results'])
        email_test.set_spam_factors(test_results['spam_factors'])
        
        db.session.add(email_test)
        db.session.commit()
        
        return render_template('inbox_test_results.html',
                             test_results=test_results,
                             domain_health=domain_health,
                             test_id=email_test.id)
    
    return render_template('inbox_test.html')

@app.route('/reports')
@login_required
def reports():
    """Analytics and reports"""
    tests = EmailTest.query.filter_by(user_id=current_user.id)\\
                          .order_by(EmailTest.created_at.desc()).all()
    
    return render_template('reports.html', tests=tests[:20])

@app.route('/settings')
@login_required
def settings():
    """User settings page"""
    return render_template('settings.html')

def check_rate_limit():
    """Check if user has exceeded rate limits"""
    plan_limits = current_user.get_plan_limits()
    tests_this_month = current_user.tests_this_month()
    
    if plan_limits['max_tests_per_month'] != -1:  # Not unlimited
        if tests_this_month >= plan_limits['max_tests_per_month']:
            return False
    
    return True

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# Initialize database
@app.before_first_request
def create_tables():
    db.create_all()
    
    # Create demo user if none exists
    if User.query.count() == 0:
        demo_user = User(
            email='demo@example.com',
            company_name='Demo Company',
            plan='professional'
        )
        demo_user.set_password('demo123')
        db.session.add(demo_user)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
'''

with open(f"{project_name}/app.py", 'w') as f:
    f.write(app_content)

print("✅ app.py created - Main Flask application")