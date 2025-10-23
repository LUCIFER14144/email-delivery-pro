# 3. Create models.py
models_content = '''from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    company_name = db.Column(db.String(100))
    plan = db.Column(db.String(20), default='starter')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    domains = db.relationship('Domain', backref='owner', lazy='dynamic')
    email_tests = db.relationship('EmailTest', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_plan_limits(self):
        from config import Config
        return Config.PLANS.get(self.plan, Config.PLANS['starter'])
    
    def can_add_domain(self):
        limits = self.get_plan_limits()
        if limits['max_domains'] == -1:  # Unlimited
            return True
        return self.domains.count() < limits['max_domains']
    
    def tests_this_month(self):
        from datetime import datetime, timedelta
        start_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0)
        return self.email_tests.filter(EmailTest.created_at >= start_of_month).count()

class Domain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domain_name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    spf_valid = db.Column(db.Boolean, default=False)
    dkim_valid = db.Column(db.Boolean, default=False)
    dmarc_valid = db.Column(db.Boolean, default=False)
    reputation_score = db.Column(db.Float, default=0.0)
    last_checked = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    email_tests = db.relationship('EmailTest', backref='domain', lazy='dynamic')
    
    def get_health_status(self):
        if self.spf_valid and self.dkim_valid and self.dmarc_valid:
            return "excellent"
        elif (self.spf_valid and self.dkim_valid) or self.reputation_score > 80:
            return "good"
        elif self.reputation_score > 60:
            return "fair"
        else:
            return "poor"

class EmailTest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    domain_id = db.Column(db.Integer, db.ForeignKey('domain.id'))
    
    # Email Details
    subject = db.Column(db.String(255))
    sender_email = db.Column(db.String(120))
    html_content = db.Column(db.Text)
    text_content = db.Column(db.Text)
    
    # Test Results
    overall_score = db.Column(db.Float, default=0.0)
    spam_score = db.Column(db.Float, default=0.0)
    delivery_rate = db.Column(db.Float, default=0.0)
    
    # Provider Results (JSON)
    provider_results = db.Column(db.Text)  # JSON string
    spam_factors = db.Column(db.Text)      # JSON string
    
    # Metadata
    test_type = db.Column(db.String(50), default='standard')  # standard, bulk, warmup
    status = db.Column(db.String(20), default='pending')      # pending, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def get_provider_results(self):
        if self.provider_results:
            return json.loads(self.provider_results)
        return []
    
    def set_provider_results(self, results):
        self.provider_results = json.dumps(results)
    
    def get_spam_factors(self):
        if self.spam_factors:
            return json.loads(self.spam_factors)
        return []
    
    def set_spam_factors(self, factors):
        self.spam_factors = json.dumps(factors)
    
    def get_status_badge(self):
        if self.overall_score >= 90:
            return {"class": "success", "text": "Excellent"}
        elif self.overall_score >= 75:
            return {"class": "warning", "text": "Good"}
        elif self.overall_score >= 60:
            return {"class": "info", "text": "Fair"}
        else:
            return {"class": "danger", "text": "Poor"}
'''

with open(f"{project_name}/models.py", 'w') as f:
    f.write(models_content)

print("✅ models.py created")