import os

filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\App.jsx"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

old_import = 'import AdminSettings from "./pages/admin/AdminSettings.jsx";'
new_import = 'import AdminSettings from "./pages/admin/AdminSettings.jsx";\nimport AdminPromos from "./pages/admin/AdminPromos.jsx";'
content = content.replace(old_import, new_import)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
print("Fixed App.jsx imports")
