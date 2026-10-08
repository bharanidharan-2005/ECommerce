import sys

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace('value: {stats?.total_revenue?.toFixed(2)},', 'value: ${stats?.total_revenue?.toFixed(2)},')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_file('src/pages/admin/AdminDashboard.jsx')
