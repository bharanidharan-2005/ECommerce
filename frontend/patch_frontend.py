import sys
sys.stdout.reconfigure(encoding='utf-8')
import os

filepath = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\ProductListPage.jsx'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. State
state_target = '''const [category, setCategory] = useState(searchParams.get("category") && searchParams.get("category") !== "all" ? searchParams.get("category") : "");
const [ordering, setOrdering] = useState(searchParams.get("sort") || (searchParams.get("sale") === "true" ? "price" : ""));'''
state_replacement = '''const [category, setCategory] = useState(searchParams.get("category") && searchParams.get("category") !== "all" ? searchParams.get("category") : "");
const [ordering, setOrdering] = useState(searchParams.get("sort") || (searchParams.get("sale") === "true" ? "price" : ""));
const [minPrice, setMinPrice] = useState(searchParams.get("minPrice") || "");
const [maxPrice, setMaxPrice] = useState(searchParams.get("maxPrice") || "");
const [inStock, setInStock] = useState(searchParams.get("inStock") === "true");'''
content = content.replace(state_target, state_replacement)

# 2. dispatch inside useEffect
effect_target = '''dispatch(fetchProducts({ page, search, category, ordering }));
    }, 350);
    return () => clearTimeout(t);
  }, [dispatch, page, search, category, ordering]);'''
effect_replacement = '''dispatch(fetchProducts({ page, search, category, ordering, minPrice, maxPrice, inStock }));
    }, 350);
    return () => clearTimeout(t);
  }, [dispatch, page, search, category, ordering, minPrice, maxPrice, inStock]);'''
content = content.replace(effect_target, effect_replacement)

# 3. hasFilters
content = content.replace(
    'const hasFilters = search || category || ordering;',
    'const hasFilters = search || category || ordering || minPrice || maxPrice || inStock;'
)

# 4. Clear All
content = content.replace(
    'setSearch(""); setCategory(""); setOrdering(""); setPage(1);',
    'setSearch(""); setCategory(""); setOrdering(""); setMinPrice(""); setMaxPrice(""); setInStock(false); setPage(1);'
)

# 5. UI Filters
sort_ui_target = '''{/* Sort */}
              <div>
                <h4 className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-3">Sort By</h4>'''
ui_replacement = '''{/* Advanced Filters */}
              <div className="mb-6 space-y-4">
                <div>
                  <h4 className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-3">Price Range</h4>
                  <div className="flex gap-2">
                    <input type="number" placeholder="Min" value={minPrice} onChange={(e) => resetAnd(setMinPrice)(e.target.value)} className="w-1/2 bg-slate-800 border-slate-700 rounded-xl px-3 py-2 text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 text-slate-200" />
                    <input type="number" placeholder="Max" value={maxPrice} onChange={(e) => resetAnd(setMaxPrice)(e.target.value)} className="w-1/2 bg-slate-800 border-slate-700 rounded-xl px-3 py-2 text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 text-slate-200" />
                  </div>
                </div>
                <label className="flex items-center gap-3 cursor-pointer group">
                  <div className={w-5 h-5 rounded border flex items-center justify-center transition-colors }>
                    {inStock && <FiX size={12} className="text-white rotate-45" />}
                  </div>
                  <span className={	ext-sm font-medium }>In Stock Only</span>
                  <input type="checkbox" className="sr-only" checked={inStock} onChange={(e) => resetAnd(setInStock)(e.target.checked)} />
                </label>
              </div>

              {/* Sort */}
              <div>
                <h4 className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-3">Sort By</h4>'''
content = content.replace(sort_ui_target, ui_replacement)

# 6. Error state retry
content = content.replace(
    'dispatch(fetchProducts({ page, search, category, ordering }))',
    'dispatch(fetchProducts({ page, search, category, ordering, minPrice, maxPrice, inStock }))'
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('Patched ProductListPage.jsx')
