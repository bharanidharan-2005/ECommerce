import sys
sys.stdout.reconfigure(encoding='utf-8')

filepath = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\features\products\productsSlice.js'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
has_import = False
for line in lines:
    if 'import { formatConvertedCurrency }' in line:
        continue
    new_lines.append(line)

new_lines.insert(2, 'import { formatConvertedCurrency } from "../../utils/currency";\n')

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print('Moved import')
