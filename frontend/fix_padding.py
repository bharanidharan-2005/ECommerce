import re

with open(r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\ProductDetailPage.jsx", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    'className="mx-auto max-w-7xl px-4 py-10 sm:px-6"',
    'className="mx-auto max-w-7xl px-4 pt-32 pb-10 sm:px-6"'
)

content = content.replace(
    'className="mx-auto max-w-7xl px-4 py-8 sm:px-6"',
    'className="mx-auto max-w-7xl px-4 pt-32 pb-8 sm:px-6"'
)

with open(r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\ProductDetailPage.jsx", "w", encoding="utf-8") as f:
    f.write(content)
print("Padding updated successfully!")
