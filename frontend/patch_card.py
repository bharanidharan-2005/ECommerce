import sys
sys.stdout.reconfigure(encoding='utf-8')
import os

filepath = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\components\BentoProductCard.jsx'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'const wishlistItems = useSelector((state) => state.wishlist.items) || [];',
    'const wishlistItems = useSelector((state) => state.wishlist.items) || [];\n  const currency = useSelector((state) => state.products.currency) || "INR";'
)
content = content.replace('formatPrice(product.price, "INR")', 'formatPrice(product.price, currency)')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('Patched BentoProductCard.jsx')
