# 1. Create requirements.txt
requirements_content = """Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Login==0.6.3
Werkzeug==2.3.7
requests==2.31.0
dnspython==2.4.2
email-validator==2.0.0
python-dotenv==1.0.0
gunicorn==21.2.0
"""

with open(f"{project_name}/requirements.txt", 'w') as f:
    f.write(requirements_content)

print("✅ requirements.txt created")