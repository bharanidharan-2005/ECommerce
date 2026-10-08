import sys
sys.stdout.reconfigure(encoding='utf-8')
import os
import re

filepath = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\features\products\productsSlice.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

target = '''const formatPrice = (priceUsd, currency, rates) => {
  if (currency === "USD") return ${Number(priceUsd).toFixed(2)};
  const rate = (rates && rates[currency]) || 1;
  const amount = Number((Number(priceUsd) * rate).toFixed(2));

  // Removed the TypeScript ": Record<string, string>" syntax
  const symbols = { USD: "", EUR: "€", GBP: "£", INR: "?", CAD: "" };
  return ${symbols[currency] || ""};
};'''

# Since spacing might be different, let's use regex
pattern = r'const formatPrice.*?return \$\{symbols\[currency\].*?;\n\};'

replacement = '''import { formatConvertedCurrency } from "../../utils/currency";

const formatPrice = (priceInr, currency, rates) => {
  // We ignore ates parameter since we don't have a /rates/ API.
  // We use the convertCurrency utility which uses hardcoded rates.
  // Base price in DB is INR.
  return formatConvertedCurrency(priceInr, "INR", currency || "INR");
};'''

new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)
print('Patched productsSlice.js')
