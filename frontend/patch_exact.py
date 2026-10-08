import sys
sys.stdout.reconfigure(encoding='utf-8')

filepath = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\features\products\productsSlice.js'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

out = []
skip = False
for line in lines:
    if 'const formatPrice = (priceUsd' in line:
        skip = True
        out.append('import { formatConvertedCurrency } from "../../utils/currency";\n')
        out.append('const formatPrice = (priceInr, currency, rates) => {\n')
        out.append('  return formatConvertedCurrency(priceInr, "INR", currency || "INR");\n')
        out.append('};\n')
        continue
    if skip:
        if line.startswith('};'):
            skip = False
        continue
    out.append(line)

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(out)
print('Patched exactly.')
