file_path = 'src/pages/admin/AdminOrders.jsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

import re

# We can just do string replacements

new_badge = '''                    className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${
                      ['delivered', 'paid'].includes(order.status)
                        ? "bg-emerald-500/10 text-emerald-400"
                        : ['shipped'].includes(order.status)
                          ? "bg-amber-500/10 text-amber-400"
                          : order.status === 'cancelled'
                            ? "bg-red-500/10 text-red-400"
                            : "bg-slate-500/10 text-slate-400"
                    }`}
                  >
                    {order.status}'''

# Replace badge (regex match since exact spacing is tricky)
content = re.sub(r'className=\{\`inline-flex items-center rounded-full px-2\.5 py-0\.5 text-xs font-medium \$\{\s*order\.status === "Completed"[\s\S]*?\}\`\}\s*>\s*\{order\.status\}', new_badge, content)


new_select = '''                  <select
                    value={order.status}
                    onChange={(e) => handleStatusChange(order.id, e.target.value)}
                    className="rounded-md border border-slate-700 bg-slate-800 px-2 py-1 text-sm text-slate-200 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                  >
                    <option value="pending">Pending</option>
                    <option value="paid">Paid</option>
                    <option value="shipped">Shipped</option>
                    <option value="delivered">Delivered</option>
                    <option value="cancelled">Cancelled</option>
                  </select>'''

content = re.sub(r'<select[\s\S]*?<\/select>', new_select, content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated AdminOrders statuses')
