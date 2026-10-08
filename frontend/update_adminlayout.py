import os

filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\admin\AdminLayout.jsx"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("[ View Store ]", "View Store")

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("Removed square brackets from View Store link.")
