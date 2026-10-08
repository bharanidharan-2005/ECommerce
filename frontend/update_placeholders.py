import os

files = [
    r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\components\ui\CartDrawer.jsx",
    r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\CheckoutPage.jsx"
]

for file_path in files:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace('placeholder="Promo code (e.g. WELCOME10)"', 'placeholder="Promo code (e.g. bharani10)"')
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
print("Updated placeholders")
