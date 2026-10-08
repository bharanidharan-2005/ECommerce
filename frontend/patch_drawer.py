import sys
sys.stdout.reconfigure(encoding='utf-8')
import os

filepath = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\components\ui\CartDrawer.jsx'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('formatPrice(FREE_SHIPPING_AT_INR - total, "INR")', 'formatPrice(FREE_SHIPPING_AT_INR - total, currency)')
content = content.replace('formatPrice(Number(item.price), "INR", rates)', 'formatPrice(Number(item.price), currency)')
content = content.replace('formatPrice(Number(item.price) * item.qty, "INR", rates)', 'formatPrice(Number(item.price) * item.qty, currency)')
content = content.replace('formatPrice(total, "INR", rates)', 'formatPrice(total, currency)')
content = content.replace('formatPrice(shippingCost, "INR", rates)', 'formatPrice(shippingCost, currency)')
content = content.replace('formatPrice(tax, "INR", rates)', 'formatPrice(tax, currency)')
content = content.replace('formatPrice(discount, "INR", rates)', 'formatPrice(discount, currency)')
content = content.replace('formatPrice(finalTotal, "INR", rates)', 'formatPrice(finalTotal, currency)')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('Patched CartDrawer.jsx')
