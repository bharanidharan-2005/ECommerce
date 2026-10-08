import os

filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\admin\AdminDashboard.jsx"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# Replace DollarSign with IndianRupee
content = content.replace("import { DollarSign, ", "import { IndianRupee, ")
content = content.replace("icon: DollarSign", "icon: IndianRupee")

# Convert sales_data revenue to INR
original_set_stats = "setStats(statsRes.data);"
new_set_stats = """const statsData = statsRes.data;
        if (statsData.sales_data) {
          statsData.sales_data = statsData.sales_data.map(item => ({
            ...item,
            revenue: parseFloat((item.revenue * 96.10).toFixed(2))
          }));
        }
        setStats(statsData);"""
content = content.replace(original_set_stats, new_set_stats)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated AdminDashboard.jsx with IndianRupee icon and converted sales_data revenue to INR.")
