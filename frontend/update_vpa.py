import os

filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\CheckoutPage.jsx"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

old_val = "value={`upi://pay?pa=pay@shopverse&pn=ShopVerse&am=${discountedTotal}&cu=INR`}"
new_val = "value={`upi://pay?pa=${import.meta.env.VITE_MERCHANT_UPI_ID || 'success@razorpay'}&pn=${import.meta.env.VITE_MERCHANT_NAME || 'ShopVerse'}&am=${discountedTotal}&cu=INR`}"

content = content.replace(old_val, new_val)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated QR code VPA")
