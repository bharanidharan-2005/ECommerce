import os

filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\ProfilePage.jsx"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("import PageTransition from \"../components/PageTransition.jsx\";", "import PageTransition from \"../components/PageTransition.jsx\";\nimport EmptyState from \"../components/ui/EmptyState.jsx\";")

old_empty = """        ) : !Array.isArray(orders) || orders.length === 0 ? (
          <motion.div
            initial={{ opacity: 0, scale: 0.97 }}
            animate={{ opacity: 1, scale: 1 }}
            className="card mx-auto max-w-md p-12 text-center"
          >
            <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-indigo-50 text-indigo-400">
              <FiPackage size={24} />
            </div>
            <p className="font-extrabold">No orders yet</p>
            <p className="mt-1 text-sm text-slate-400">Your purchases will appear here.</p>
            <Link to="/products" className="btn-primary mt-6">Start shopping</Link>
          </motion.div>
        ) : ("""

new_empty = """        ) : !Array.isArray(orders) || orders.length === 0 ? (
          <EmptyState 
            icon="inbox"
            title="No orders yet"
            message="Your purchases will appear here."
            actionText="Start shopping"
            actionLink="/products"
          />
        ) : ("""

content = content.replace(old_empty, new_empty)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated ProfilePage empty state")
