file_path = 'src/pages/admin/AdminOrders.jsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Capitalize the displayed status
content = re.sub(r'\{order\.status\}', '{order.status.charAt(0).toUpperCase() + order.status.slice(1)}', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated AdminOrders statuses display')
