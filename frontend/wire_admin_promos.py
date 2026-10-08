import os

app_path = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\App.jsx"
with open(app_path, "r", encoding="utf-8") as f:
    app_content = f.read()

app_content = app_content.replace('import AdminSettings from "./pages/admin/AdminSettings";', 'import AdminSettings from "./pages/admin/AdminSettings";\nimport AdminPromos from "./pages/admin/AdminPromos";')
app_content = app_content.replace('<Route path="settings" element={<AdminSettings />} />', '<Route path="settings" element={<AdminSettings />} />\n              <Route path="promos" element={<AdminPromos />} />')

with open(app_path, "w", encoding="utf-8") as f:
    f.write(app_content)

layout_path = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\admin\AdminLayout.jsx"
with open(layout_path, "r", encoding="utf-8") as f:
    layout_content = f.read()

layout_content = layout_content.replace('import { FiHome, FiBox, FiUsers, FiShoppingBag, FiSettings, FiMenu, FiX, FiPieChart } from "react-icons/fi";', 'import { FiHome, FiBox, FiUsers, FiShoppingBag, FiSettings, FiMenu, FiX, FiPieChart, FiTag } from "react-icons/fi";')
layout_content = layout_content.replace('{ name: "Settings", path: "/admin/settings", icon: FiSettings },', '{ name: "Promo Codes", path: "/admin/promos", icon: FiTag },\n    { name: "Settings", path: "/admin/settings", icon: FiSettings },')

with open(layout_path, "w", encoding="utf-8") as f:
    f.write(layout_content)

print("Updated App.jsx and AdminLayout.jsx")
