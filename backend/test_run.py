import os
import sys

# Add the backend directory to path
sys.path.insert(0, r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend')

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

import django
print(f"Python path: {sys.path[0]}")
print(f"Config dir exists: {os.path.exists(r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\config')}")

django.setup()
print(' Django setup OK')