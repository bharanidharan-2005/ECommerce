file_path = 'src/pages/admin/AdminProducts.jsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('Price (USD)', 'Price (₹)')
content = content.replace('formData.append("price", newProduct.price);', 'formData.append("price", (parseFloat(newProduct.price) / 96.10).toFixed(2));')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated Add Product for INR to USD conversion")
