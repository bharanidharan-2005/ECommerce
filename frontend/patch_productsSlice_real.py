import sys
import re
sys.stdout.reconfigure(encoding='utf-8')

filepath = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\features\products\productsSlice.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'const formatPrice = \(priceUsd, currency, rates\) => \{.*?return \$\{symbols\[currency\] \|\| "\$"\}.*?;\n\};'

replacement = '''import { formatConvertedCurrency } from "../../utils/currency";

const formatPrice = (priceInr, currency, rates) => {
  return formatConvertedCurrency(priceInr, "INR", currency || "INR");
};'''

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patched productsSlice.js!")
