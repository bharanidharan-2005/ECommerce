import sys
sys.stdout.reconfigure(encoding='utf-8')
import os

filepath = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\components\Navbar.jsx'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('import { setCurrency } from "../features/products/productsSlice";', 'import { setCurrency } from "../features/ui/uiSlice";')
content = content.replace('const currentCurrency = useSelector((state) => state.products.currency);', 'const currentCurrency = useSelector((state) => state.ui.currency);')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('Patched Navbar.jsx to use uiSlice')
