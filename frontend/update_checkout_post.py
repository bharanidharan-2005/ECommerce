import re

file_path = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\CheckoutPage.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_post = """        const { data } = await api.post("/orders/checkout/", {
          ...address,
          payment_method: method,
          upi_id: method.startsWith("upi_") ? upiId : "",
          items: items.map((i) => ({ product_id: i.id, quantity: i.qty })),
        });"""

new_post = """        const { data } = await api.post("/orders/checkout/", {
          ...address,
          payment_method: method,
          upi_id: method.startsWith("upi_") ? upiId : "",
          items: items.map((i) => ({ product_id: i.id, quantity: i.qty })),
          promo_code_str: coupon ? coupon.code : null,
        });"""

content = content.replace(old_post, new_post)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated CheckoutPage.jsx placeOrder")
