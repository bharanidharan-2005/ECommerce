import os

filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\CheckoutPage.jsx"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

old_navigate_1 = 'navigate("/order-success", { state: { orderId: data.order.order_number, total: data.order.total_price } });'
new_navigate_1 = 'navigate(`/order-success/${data.order.order_number}?method=${method}`, { state: { orderId: data.order.order_number, total: data.order.total_price } });'

content = content.replace(old_navigate_1, new_navigate_1)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated navigation paths in CheckoutPage")
