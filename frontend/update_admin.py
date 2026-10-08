import os
import re

def update_file(filepath, empty_state_icon, empty_state_title, empty_state_msg):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Import EmptyState if not present
    if "EmptyState" not in content:
        import_stmt = 'import EmptyState from "../../components/ui/EmptyState";\n'
        content = re.sub(r'(import React.*?\n)', r'\1' + import_stmt, content)

    # Find the table body zero-state
    if "filteredOrders.length === 0" in content:
        pattern = r'\{\s*filteredOrders\.length === 0 \? \([\s\S]*?\) : '
        replacement = f"""{{filteredOrders.length === 0 ? (
                <tr>
                  <td colSpan="10" className="py-8">
                    <EmptyState 
                      icon={{{empty_state_icon}}} 
                      title="{empty_state_title}" 
                      message={{searchQuery ? "Try adjusting your search" : "{empty_state_msg}"}}
                      actionText={{searchQuery ? "Clear Search" : undefined}}
                      onAction={{() => setSearchQuery("")}}
                    />
                  </td>
                </tr>
              ) : """
        content = re.sub(pattern, replacement, content)
        
    elif "filteredProducts.length === 0" in content:
        pattern = r'\{\s*filteredProducts\.length === 0 \? \([\s\S]*?\) : '
        replacement = f"""{{filteredProducts.length === 0 ? (
                <tr>
                  <td colSpan="10" className="py-8">
                    <EmptyState 
                      icon={{{empty_state_icon}}} 
                      title="{empty_state_title}" 
                      message={{searchQuery ? "Try adjusting your search" : "{empty_state_msg}"}}
                      actionText={{searchQuery ? "Clear Search" : undefined}}
                      onAction={{() => setSearchQuery("")}}
                    />
                  </td>
                </tr>
              ) : """
        content = re.sub(pattern, replacement, content)
        
    elif "filteredCustomers.length === 0" in content:
        pattern = r'\{\s*filteredCustomers\.length === 0 \? \([\s\S]*?\) : '
        replacement = f"""{{filteredCustomers.length === 0 ? (
                <tr>
                  <td colSpan="10" className="py-8">
                    <EmptyState 
                      icon={{{empty_state_icon}}} 
                      title="{empty_state_title}" 
                      message={{searchQuery ? "Try adjusting your search" : "{empty_state_msg}"}}
                      actionText={{searchQuery ? "Clear Search" : undefined}}
                      onAction={{() => setSearchQuery("")}}
                    />
                  </td>
                </tr>
              ) : """
        content = re.sub(pattern, replacement, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


# AdminOrders
filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\admin\AdminOrders.jsx"
with open(filepath, 'r', encoding='utf-8') as f: content = f.read()
if "EmptyState" not in content:
    content = content.replace('import { motion', 'import EmptyState from "../../components/ui/EmptyState";\nimport { motion')
    pattern = r'\{\s*filteredOrders\.length === 0 \? \([\s\S]*?\) : filteredOrders\.map'
    replacement = """{filteredOrders.length === 0 ? (
                <tr>
                  <td colSpan="10" className="py-8">
                    <EmptyState 
                      icon={FiPackage} 
                      title="No orders found" 
                      message={searchQuery || statusFilter !== 'all' ? "Try adjusting your filters" : "You haven't received any orders yet."}
                      actionText={searchQuery || statusFilter !== 'all' ? "Clear Filters" : undefined}
                      onAction={() => { setSearchQuery(""); setStatusFilter("all"); }}
                    />
                  </td>
                </tr>
              ) : filteredOrders.map"""
    content = re.sub(pattern, replacement, content)
    with open(filepath, 'w', encoding='utf-8') as f: f.write(content)

# AdminProducts
filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\admin\AdminProducts.jsx"
with open(filepath, 'r', encoding='utf-8') as f: content = f.read()
if "EmptyState" not in content:
    content = content.replace('import { motion', 'import EmptyState from "../../components/ui/EmptyState";\nimport { motion')
    pattern = r'\{\s*filteredProducts\.length === 0 \? \([\s\S]*?\) : filteredProducts\.map'
    replacement = """{filteredProducts.length === 0 ? (
                <tr>
                  <td colSpan="10" className="py-8">
                    <EmptyState 
                      icon={FiBox} 
                      title="No products found" 
                      message={searchQuery ? "Try adjusting your search" : "Add some products to your store."}
                      actionText={searchQuery ? "Clear Search" : undefined}
                      onAction={() => setSearchQuery("")}
                    />
                  </td>
                </tr>
              ) : filteredProducts.map"""
    content = re.sub(pattern, replacement, content)
    with open(filepath, 'w', encoding='utf-8') as f: f.write(content)

# AdminCustomers
filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\admin\AdminCustomers.jsx"
with open(filepath, 'r', encoding='utf-8') as f: content = f.read()
if "EmptyState" not in content:
    content = content.replace('import { format }', 'import EmptyState from "../../components/ui/EmptyState";\nimport { format }')
    pattern = r'\{\s*filteredCustomers\.length === 0 \? \([\s\S]*?\) : filteredCustomers\.map'
    replacement = """{filteredCustomers.length === 0 ? (
                <tr>
                  <td colSpan="10" className="py-8">
                    <EmptyState 
                      icon={FiUsers} 
                      title="No customers found" 
                      message={searchQuery ? "Try adjusting your search" : "No customers have registered yet."}
                      actionText={searchQuery ? "Clear Search" : undefined}
                      onAction={() => setSearchQuery("")}
                    />
                  </td>
                </tr>
              ) : filteredCustomers.map"""
    content = re.sub(pattern, replacement, content)
    with open(filepath, 'w', encoding='utf-8') as f: f.write(content)

print("Updated admin pages to use EmptyState")
