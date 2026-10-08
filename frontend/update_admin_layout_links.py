import re

file_path = "src/pages/admin/AdminLayout.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Update navItems
content = content.replace('to: "#customers"', 'to: "/admin/customers"')
content = content.replace('to: "#analytics"', 'to: "/admin/analytics"')
content = content.replace('to: "#settings"', 'to: "/admin/settings"')

# Fix active class logic
content = content.replace('isActive && to !== "#customers" && to !== "#analytics"', 'isActive')

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated AdminLayout.jsx links")
