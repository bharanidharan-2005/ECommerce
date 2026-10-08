import sys

filepath = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\ProductListPage.jsx'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

target_empty = '''            {!loading && !error && items.length === 0 && (
              <EmptyState 
                icon="search"
                title="No matching products"
                message="We couldn't find anything matching your current filters. Try adjusting your search criteria."
                actionText={hasFilters ? "Clear all filters" : null}
                actionOnClick={() => { setSearch(""); setCategory(""); setOrdering(""); setMinPrice(""); setMaxPrice(""); setInStock(false); setPage(1); }}
              />
            )}'''

replacement_empty = '''            {!loading && !error && items.length === 0 && isSale && (
              <EmptyState 
                icon="search"
                title="No active deals right now."
                message="We're preparing new offers for you."
                actionText="Explore All Products"
                actionOnClick={() => { window.location.href = '/products'; }}
              />
            )}
            {!loading && !error && items.length === 0 && !isSale && (
              <EmptyState 
                icon="search"
                title="No matching products"
                message="We couldn't find anything matching your current filters. Try adjusting your search criteria."
                actionText={hasFilters ? "Clear all filters" : null}
                actionOnClick={() => { setSearch(""); setCategory(""); setOrdering(""); setMinPrice(""); setMaxPrice(""); setInStock(false); setPage(1); }}
              />
            )}'''

content = content.replace(target_empty, replacement_empty)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated empty state in ProductListPage.jsx')
