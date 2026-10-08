file_path = 'src/components/HeaderCountryCurrency.jsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('INR ?', 'INR ₹')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
