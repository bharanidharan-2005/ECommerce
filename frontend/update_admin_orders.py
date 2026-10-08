file_path = 'src/pages/admin/AdminOrders.jsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add import
if 'formatConvertedCurrency' not in content:
    content = content.replace('import { format } from "date-fns";', 'import { format } from "date-fns";\nimport { formatConvertedCurrency } from "../../utils/currency";')

# Replace totals
content = content.replace('${parseFloat(order.total_price).toFixed(2)}', '{formatConvertedCurrency(order.total_price)}')
content = content.replace('${parseFloat(item.subtotal).toFixed(2)}', '{formatConvertedCurrency(item.subtotal)}')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated AdminOrders.jsx")
