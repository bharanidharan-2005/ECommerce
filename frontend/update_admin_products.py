file_path = 'src/pages/admin/AdminProducts.jsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'formatConvertedCurrency' not in content:
    content = content.replace('import api from "../../api/axios";', 'import api from "../../api/axios";\nimport { formatConvertedCurrency } from "../../utils/currency";')

content = content.replace('${parseFloat(product.price).toFixed(2)}', '{formatConvertedCurrency(product.price)}')
content = content.replace('Price ($)', 'Price (USD)')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated AdminProducts.jsx")
