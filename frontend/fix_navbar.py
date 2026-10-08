import sys
import re

filepath = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\components\Navbar.jsx'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the Link that wraps currentCategoryLabel with a button
# We need to find:
#            <Link 
#              to="/products?category=all" 
#              className={`transition flex items-center gap-1 ${location.search.includes('category=') ? 'text-indigo-400 border-b-2 border-indigo-400' : 'hover:text-indigo-400'}`}
#            >
#              {currentCategoryLabel} <FiChevronDown ... />
#            </Link>
# And change it to a <button>

pattern = r'<Link\s+to="/products\?category=all"\s+className={`transition flex items-center gap-1 \$\{location\.search\.includes\(\'category=\'\)\s*\?\s*\'text-indigo-400 border-b-2 border-indigo-400\'\s*:\s*\'hover:text-indigo-400\'\}`}\s*>\s*\{currentCategoryLabel\}\s*<FiChevronDown[^>]+>\s*</Link>'

def replacement(match):
    return """<button 
              className={`transition flex items-center gap-1 ${location.search.includes('category=') ? 'text-indigo-400 border-b-2 border-indigo-400' : 'hover:text-indigo-400'}`}
            >
              {currentCategoryLabel} <FiChevronDown size={14} className={`transition-transform ${isCategoriesMegaMenuOpen ? 'rotate-180' : ''}`} />
            </button>"""

new_content = re.sub(pattern, replacement, content, count=1)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Navbar updated")
