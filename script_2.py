# 2. Create config.py
config_content = '''import os
from datetime import timedelta

class Config:
    # Flask Settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
    
    # Database Settings
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///deliverability.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Email Testing APIs (Add your own keys)
    MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY') or 'your-mailgun-key'
    MAILGUN_DOMAIN = os.environ.get('MAILGUN_DOMAIN') or 'your-domain.com'
    
    # Session Settings
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)
    
    # Rate Limiting
    MAX_TESTS_PER_HOUR = 10
    MAX_TESTS_PER_DAY = 50
    
    # Subscription Plans
    PLANS = {
        'starter': {
            'name': 'Starter',
            'price': 49,
            'max_domains': 5,
            'max_tests_per_month': 100,
            'features': ['Basic reporting', 'Email support']
        },
        'professional': {
            'name': 'Professional', 
            'price': 149,
            'max_domains': 25,
            'max_tests_per_month': 500,
            'features': ['Advanced analytics', 'API access', 'Priority support']
        },
        'enterprise': {
            'name': 'Enterprise',
            'price': 399,
            'max_domains': -1,  # Unlimited
            'max_tests_per_month': -1,  # Unlimited
            'features': ['Custom integrations', 'Dedicated support', 'White-label option']
        }
    }

class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
'''

with open(f"{project_name}/config.py", 'w') as f:
    f.write(config_content)

print("✅ config.py created")