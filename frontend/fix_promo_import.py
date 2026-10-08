import os

filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\admin\AdminPromos.jsx"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace('import api from "../../services/api";', 'import api from "../../api/axios";')

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
print("Fixed API import in AdminPromos.jsx")
