import sys
sys.stdout.reconfigure(encoding='utf-8')
import os

filepath = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\components\Navbar.jsx'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if 'import { useDispatch, useSelector } from "react-redux";' in line:
        new_lines.append(line)
        new_lines.append('import { setCurrency } from "../features/products/productsSlice";\n')
    elif 'const [selectedCurrency, setSelectedCurrency] = useState(currencies[0]);' in line:
        new_lines.append('  const currentCurrency = useSelector((state) => state.products.currency);\n')
        new_lines.append('  const selectedCurrency = currencies.find(c => c.code === currentCurrency) || currencies[0];\n')
    elif 'setSelectedCurrency(c)' in line:
        new_lines.append(line.replace('setSelectedCurrency(c)', 'dispatch(setCurrency(c.code))'))
    else:
        new_lines.append(line)

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print('Patched Navbar.jsx')
