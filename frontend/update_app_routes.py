import re

file_path = "src/App.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add imports
imports = """
import AdminProducts from "./pages/admin/AdminProducts.jsx";
import AdminCustomers from "./pages/admin/AdminCustomers.jsx";
import AdminAnalytics from "./pages/admin/AdminAnalytics.jsx";
import AdminSettings from "./pages/admin/AdminSettings.jsx";
"""
content = content.replace('import AdminProducts from "./pages/admin/AdminProducts.jsx";', imports.strip())

# Add routes
routes = """
              <Route path="products" element={<AdminProducts />} />
              <Route path="customers" element={<AdminCustomers />} />
              <Route path="analytics" element={<AdminAnalytics />} />
              <Route path="settings" element={<AdminSettings />} />
"""
content = content.replace('<Route path="products" element={<AdminProducts />} />', routes.strip())

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated App.jsx with new routes")
