import sys
sys.stdout.reconfigure(encoding='utf-8')
import os

filepath = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\components\BentoProductCard.jsx'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('const currency = useSelector((state) => state.products.currency) || "INR";', 'const currency = useSelector((state) => state.ui.currency) || "INR";')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('Patched BentoProductCard.jsx to use uiSlice')
