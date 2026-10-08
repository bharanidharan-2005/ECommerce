import os

file_path = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\ProfilePage.jsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace potentially crashing lines
content = content.replace(
    'const isCOD = order.payment_method === "cod";',
    'const isCOD = order?.payment_method === "cod";'
)
content = content.replace(
    'let current = stages.findIndex(s => s.id === order.status);',
    'let current = stages.findIndex(s => s.id === order?.status);'
)
content = content.replace(
    'const cancelled = order.status === "cancelled";',
    'const cancelled = order?.status === "cancelled";'
)
content = content.replace(
    '{order.payment_method.toUpperCase().replace(\'_\', \' \')}',
    '{(order.payment_method || "unknown").toUpperCase().replace(\'_\', \' \')}'
)
content = content.replace(
    'order.items.map(it => (',
    '(order.items || []).map(it => ('
)
content = content.replace(
    'order.items.length',
    '(o.items || []).length'
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Made OrderDetails crash-proof")
