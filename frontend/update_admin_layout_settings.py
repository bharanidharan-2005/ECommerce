import re

file_path = "src/pages/admin/AdminLayout.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace('to="#settings"', 'to="/admin/settings"')

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated Settings link in AdminLayout.jsx")
