import sys

filepath = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\ProductListPage.jsx'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. State and effect replacements
target_states = '''  const [page, setPage] = useState(1);
  const [search, setSearch] = useState(searchParams.get('q') || '');
  const [category, setCategory] = useState("");
  const [ordering, setOrdering] = useState("");
  const [minPrice, setMinPrice] = useState("");
  const [maxPrice, setMaxPrice] = useState("");
  const [inStock, setInStock] = useState(false);'''

replacement_states = '''  const [page, setPage] = useState(1);
  const [search, setSearch] = useState(searchParams.get('q') || '');
  const [category, setCategory] = useState("");
  const [ordering, setOrdering] = useState("");
  const [minPrice, setMinPrice] = useState("");
  const [maxPrice, setMaxPrice] = useState("");
  const [inStock, setInStock] = useState(false);
  const isSale = searchParams.get('sale') === 'true';'''

content = content.replace(target_states, replacement_states)

target_effect = '''  useEffect(() => {
    const t = setTimeout(() => {
      dispatch(fetchProducts({ page, search, category, ordering, minPrice, maxPrice, inStock }));
    }, 350);
    return () => clearTimeout(t);
  }, [dispatch, page, search, category, ordering, minPrice, maxPrice, inStock]);

  const hasFilters = search || category || ordering || minPrice || maxPrice || inStock;'''

replacement_effect = '''  useEffect(() => {
    const t = setTimeout(() => {
      dispatch(fetchProducts({ page, search, category, ordering, min_price: minPrice, max_price: maxPrice, in_stock: inStock, sale: isSale }));
    }, 350);
    return () => clearTimeout(t);
  }, [dispatch, page, search, category, ordering, minPrice, maxPrice, inStock, isSale]);

  const hasFilters = search || category || ordering || minPrice || maxPrice || inStock;'''

content = content.replace(target_effect, replacement_effect)

target_header = '''        {/* Header Section */}
        <div className="mb-10 text-center sm:text-left sm:flex sm:items-end sm:justify-between">
          <div>
            <h1 className="text-4xl font-black tracking-tight sm:text-5xl text-slate-100 mb-2">The Collection</h1>
            <p className="text-slate-400 text-lg">
              {loading ? "Curating our finest pieces..." : Showing  extraordinary items}
            </p>
          </div>'''

replacement_header = '''        {/* Header Section */}
        <div className="mb-10 text-center sm:text-left sm:flex sm:items-end sm:justify-between">
          <div>
            <h1 className="text-4xl font-black tracking-tight sm:text-5xl text-slate-100 mb-2">
              {isSale ? "Today's Tech Deals" : "The Collection"}
            </h1>
            <p className="text-slate-400 text-lg">
              {isSale ? (
                <>
                  <span className="block mb-1">Save more on gaming, electronics and tech essentials.</span>
                  {loading ? "Finding the best deals..." : ${count || items.length} products currently on sale}
                </>
              ) : (
                loading ? "Curating our finest pieces..." : Showing  extraordinary items
              )}
            </p>
          </div>'''

content = content.replace(target_header, replacement_header)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated ProductListPage.jsx')
