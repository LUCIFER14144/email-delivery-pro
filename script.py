# Let me recreate the complete project and zip file for download

import os
import zipfile

# Create project directory
project_name = "email-deliverability-saas"
if os.path.exists(project_name):
    import shutil
    shutil.rmtree(project_name)

os.makedirs(project_name, exist_ok=True)
os.makedirs(f"{project_name}/utils", exist_ok=True) 
os.makedirs(f"{project_name}/templates", exist_ok=True)
os.makedirs(f"{project_name}/static/css", exist_ok=True)
os.makedirs(f"{project_name}/static/js", exist_ok=True)

print(f"✅ Created project structure: {project_name}/")
print("📁 Folders created:")
print("  - utils/")
print("  - templates/")
print("  - static/css/")
print("  - static/js/")