import re

file_path = "src/pages/admin/AdminProducts.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace the state and useEffect
new_state_and_effect = """
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  
  const [newProduct, setNewProduct] = useState({
    name: "",
    description: "",
    price: "",
    stock: "",
    category: "",
    image: null
  });

  const fetchData = async (page = 1) => {
    setLoading(true);
    try {
      const [prodRes, catRes] = await Promise.all([
        api.get(`/products/?page=${page}`),
        api.get("/products/categories/")
      ]);
      setProducts(prodRes.data.results || prodRes.data);
      if (prodRes.data.count) {
        setTotalPages(Math.ceil(prodRes.data.count / 12));
      }
      setCategories(catRes.data.results || catRes.data);
    } catch (err) {
      toast.error("Failed to load data");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData(currentPage);
  }, [currentPage]);
"""

# Replace the block from `const [products, setProducts] = useState([]);` to `}, []);`
content = re.sub(
    r'const \[products, setProducts\] = useState\(\[\]\);.*?}, \[\]\);',
    new_state_and_effect.strip(),
    content,
    flags=re.DOTALL
)

# Add pagination controls at the bottom of the table
pagination_controls = """
      </div>

      {totalPages > 1 && (
        <div className="flex items-center justify-between mt-6 px-4">
          <button 
            disabled={currentPage === 1}
            onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
            className="rounded-lg border border-slate-700 bg-slate-800/50 px-4 py-2 text-sm font-medium text-slate-300 hover:bg-slate-800 disabled:opacity-50"
          >
            Previous
          </button>
          <span className="text-sm text-slate-400">Page {currentPage} of {totalPages}</span>
          <button 
            disabled={currentPage === totalPages}
            onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
            className="rounded-lg border border-slate-700 bg-slate-800/50 px-4 py-2 text-sm font-medium text-slate-300 hover:bg-slate-800 disabled:opacity-50"
          >
            Next
          </button>
        </div>
      )}

      {showAddModal && (
"""

content = content.replace("</div>\n\n      {showAddModal && (", pagination_controls)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Pagination added to AdminProducts.jsx")
