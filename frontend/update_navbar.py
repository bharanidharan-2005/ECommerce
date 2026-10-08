import sys

filepath = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\components\Navbar.jsx'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Define the classes
target_classes_def = '''export default function Navbar() {
  const dispatch = useDispatch();'''

replacement_classes_def = '''export default function Navbar() {
  const dispatch = useDispatch();
  const activeNavClass = "text-indigo-300 font-bold bg-indigo-500/10 px-3 py-1.5 rounded-lg shadow-[0_0_10px_rgba(99,102,241,0.15)] transition-all duration-200";
  const inactiveNavClass = "text-slate-300 font-medium px-3 py-1.5 rounded-lg hover:bg-slate-800 hover:text-indigo-300 transition-all duration-200";'''

content = content.replace(target_classes_def, replacement_classes_def)

# Link 1: Shop
target_shop = '''          <Link
            to="/products"
            className={	ransition py-2 }
          >'''
replacement_shop = '''          <Link
            to="/products"
            className={location.pathname === '/products' && !location.search ? activeNavClass : inactiveNavClass}
          >'''
content = content.replace(target_shop, replacement_shop)

# Link 2: Categories
target_categories = '''          <div
            className="relative py-2"
            onMouseEnter={() => setIsCategoriesMegaMenuOpen(true)}
            onMouseLeave={() => setIsCategoriesMegaMenuOpen(false)}
          >
            <Link
              to="/products?category=all"
              className={	ransition flex items-center gap-1 }
            >'''
replacement_categories = '''          <div
            className="relative"
            onMouseEnter={() => setIsCategoriesMegaMenuOpen(true)}
            onMouseLeave={() => setIsCategoriesMegaMenuOpen(false)}
          >
            <Link
              to="/products?category=all"
              className={lex items-center gap-1 }
            >'''
content = content.replace(target_categories, replacement_categories)

# Link 3: New Arrivals
target_new_arrivals = '''          <Link
            to="/products?sort=-created_at"
            className={	ransition py-2 }
          >'''
replacement_new_arrivals = '''          <Link
            to="/products?sort=-created_at"
            className={location.search.includes('sort=-created_at') ? activeNavClass : inactiveNavClass}
          >'''
content = content.replace(target_new_arrivals, replacement_new_arrivals)

# Link 4: Deals
target_deals = '''          <Link
            to="/products?sale=true"
            className={	ransition py-2 }
          >'''
replacement_deals = '''          <Link
            to="/products?sale=true"
            className={location.search.includes('sale=true') ? activeNavClass : inactiveNavClass}
          >'''
content = content.replace(target_deals, replacement_deals)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated Navbar.jsx')
