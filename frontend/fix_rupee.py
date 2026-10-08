file_path = 'src/pages/admin/AdminDashboard.jsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace("`?${value", "`₹${value")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
