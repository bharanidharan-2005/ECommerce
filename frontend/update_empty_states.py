import os

filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\ProductListPage.jsx"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("import BentoProductCard from \"../components/BentoProductCard.jsx\";", "import BentoProductCard from \"../components/BentoProductCard.jsx\";\nimport EmptyState from \"../components/ui/EmptyState.jsx\";\nimport ErrorState from \"../components/ui/ErrorState.jsx\";")

old_error = "{error && <div className=\"rounded-2xl bg-red-500/10 border border-red-500/20 p-4 mb-6 text-sm font-medium text-red-400\">{error}</div>}"
new_error = "{error && <div className=\"mb-6\"><ErrorState message={error} onRetry={() => dispatch(fetchProducts({ page, search, category, ordering }))} /></div>}"
content = content.replace(old_error, new_error)

old_empty = """            {!loading && !error && items.length === 0 && (
              <div className="mx-auto max-w-md py-20 text-center">
                <div className="w-20 h-20 bg-slate-800 rounded-full flex items-center justify-center mx-auto mb-6">
                  <FiSearch size={32} className="text-slate-500" />
                </div>
                <h3 className="text-xl font-bold text-slate-200 mb-2">No matching products</h3>
                <p className="text-slate-400 text-sm">We couldn't find anything matching your current filters. Try adjusting your search criteria.</p>
                {hasFilters && (
                  <button onClick={() => { setSearch(""); setCategory(""); setOrdering(""); setPage(1); }} className="mt-6 px-6 py-2.5 rounded-full border border-slate-700 text-slate-300 font-medium hover:bg-slate-800 transition-colors">
                    Clear all filters
                  </button>
                )}
              </div>
            )}"""
            
new_empty = """            {!loading && !error && items.length === 0 && (
              <EmptyState 
                icon="search"
                title="No matching products"
                message="We couldn't find anything matching your current filters. Try adjusting your search criteria."
                actionText={hasFilters ? "Clear all filters" : null}
                actionOnClick={() => { setSearch(""); setCategory(""); setOrdering(""); setPage(1); }}
              />
            )}"""

content = content.replace(old_empty, new_empty)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\WishlistPage.jsx"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("import BentoProductCard from \"../components/BentoProductCard.jsx\";", "import BentoProductCard from \"../components/BentoProductCard.jsx\";\nimport EmptyState from \"../components/ui/EmptyState.jsx\";")

old_empty = """        {items.length === 0 ? (
          <motion.div
            initial={{ opacity: 0, scale: 0.97 }}
            animate={{ opacity: 1, scale: 1 }}
            className="card mx-auto max-w-md p-12 text-center"
          >
            <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-rose-50 text-rose-400">
              <FiHeart size={24} />
            </div>
            <p className="font-extrabold text-xl">Your wishlist is empty</p>
            <p className="mt-2 text-sm text-slate-400">
              Save your favorite items here while you shop.
            </p>
            <Link to="/products" className="btn-primary mt-6 !px-6">
              <FiShoppingBag size={16} /> Continue Shopping
            </Link>
          </motion.div>
        ) : ("""

new_empty = """        {items.length === 0 ? (
          <EmptyState 
             title="Your wishlist is empty"
             message="Save your favorite items here while you shop."
             actionText="Continue Shopping"
             actionLink="/products"
          />
        ) : ("""

content = content.replace(old_empty, new_empty)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated ProductListPage and WishlistPage")
