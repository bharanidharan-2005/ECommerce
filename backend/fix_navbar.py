
import sys
filepath = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\components\Navbar.jsx'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(' border-b-2 border-indigo-400', ' font-bold')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('Done!')

