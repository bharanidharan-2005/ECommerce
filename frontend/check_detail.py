import os

filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\ProductDetailPage.jsx"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Check wishlist references in ProductDetailPage
for line in content.splitlines():
    if "isWishlisted" in line or "handleWishlist" in line or "toggleWishlist" in line:
        print(line.strip())

