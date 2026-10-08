import re

with open(r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\components\Navbar.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Fix the dead zone by wrapping the visual menu in a div and using pt-2 on the motion.div
old_mega_menu = """                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 10 }}
                  transition={{ duration: 0.15 }}
                  className="absolute left-1/2 -translate-x-1/2 top-full mt-2 w-48 rounded-xl border border-slate-700 bg-slate-800 p-2 shadow-xl shadow-slate-900/50"
                >
                  <div className="flex flex-col gap-1">"""

new_mega_menu = """                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 10 }}
                  transition={{ duration: 0.15 }}
                  className="absolute left-1/2 -translate-x-1/2 top-full pt-2 w-48"
                >
                  <div className="rounded-xl border border-slate-700 bg-slate-800 p-2 shadow-xl shadow-slate-900/50 flex flex-col gap-1">"""

content = content.replace(old_mega_menu, new_mega_menu)

with open(r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\components\Navbar.jsx", "w", encoding="utf-8") as f:
    f.write(content)
print("Dead zone fixed!")
