import os

filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\admin\AdminProducts.jsx"

content = """import { useState, useEffect } from "react";
import api from "../../api/axios";
import { formatConvertedCurrency } from "../../utils/currency";
import { Plus, Edit, Trash2, X, Eye, Search, Filter, PackageOpen } from "lucide-react";
import toast from "react-hot-toast";

const mediaUrl = (path) => {
  if (!path) return "";
  if (/^https?:\\/\\//i.test(path)) return path;
  const base = (import.meta.env.VITE_API_URL || "http://localhost:8010/api").replace(/\\/api$/, "");
  return base + path;
};

export default function AdminProducts() {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [searchQuery, setSearchQuery] = useState("");
  const [categoryFilter, setCategoryFilter] = useState("all");
  
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

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this product?")) return;
    try {
      await api.delete("/products/" + id + "/");
      toast.success("Product deleted");
      setProducts(products.filter(p => p.id !== id));
    } catch (err) {
      toast.error("Failed to delete product");
    }
  };

  const handleAddSubmit = async (e) => {
    e.preventDefault();
    if (!newProduct.category) {
      toast.error("Please select a category");
      return;
    }
    const formData = new FormData();
    formData.append("name", newProduct.name);
    formData.append("description", newProduct.description);
    // Remove the inverse conversion (we will rely on backend to handle it, or we just submit exact price because it's entered in INR)
    // Wait, earlier it was parseFloat(newProduct.price) / 96.10, but if we assume all values are in INR, and backend expects USD, 
    // it's tricky. Let's keep the existing conversion logic to avoid breaking it. 
    formData.append("price", (parseFloat(newProduct.price) / 96.10).toFixed(2));
    formData.append("stock", newProduct.stock);
    formData.append("category", newProduct.category);
    if (newProduct.image) formData.append("image", newProduct.image);

    try {
      const res = await api.post("/products/", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      setProducts([res.data, ...products]);
      setShowAddModal(false);
      toast.success("Product added successfully");
      setNewProduct({ name: "", description: "", price: "", stock: "", category: "", image: null });
    } catch (err) {
      toast.error("Failed to add product");
    }
  };

  const filteredProducts = products.filter(product => {
    const matchesSearch = product.name.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = categoryFilter === "all" || product.category?.toString() === categoryFilter || product.category_name === categoryFilter;
    return matchesSearch && matchesCategory;
  });

  if (loading && products.length === 0) {
    return <div className="text-center py-12 text-slate-400">Loading products...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <h1 className="text-2xl font-bold text-slate-100">Products</h1>
        <div className="flex flex-col sm:flex-row items-center gap-3 w-full sm:w-auto">
          <div className="relative w-full sm:w-64">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 h-4 w-4" />
            <input 
              type="text" 
              placeholder="Search products..." 
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full rounded-lg border border-slate-700 bg-slate-800/50 pl-10 pr-4 py-2 text-sm text-slate-200 placeholder-slate-400 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
            />
          </div>
          
          <div className="relative w-full sm:w-auto flex items-center gap-2">
            <Filter className="text-slate-400 h-4 w-4" />
            <select
              value={categoryFilter}
              onChange={(e) => setCategoryFilter(e.target.value)}
              className="w-full sm:w-auto rounded-lg border border-slate-700 bg-slate-800/50 px-3 py-2 text-sm text-slate-200 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
            >
              <option value="all">All Categories</option>
              {categories.map(c => (
                <option key={c.id} value={c.name}>{c.name}</option>
              ))}
            </select>
          </div>
          
          <button 
            onClick={() => setShowAddModal(true)}
            className="w-full sm:w-auto flex items-center justify-center gap-2 rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-indigo-700"
          >
            <Plus className="h-4 w-4" />
            Add Product
          </button>
        </div>
      </div>

      <div className="overflow-hidden rounded-xl border border-slate-800 bg-slate-900 shadow-xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-400">
            <thead className="border-b border-slate-800 bg-slate-900/50 text-xs uppercase text-slate-300">
              <tr>
                <th className="px-6 py-4 font-semibold">Product</th>
                <th className="px-3 py-4 font-semibold">Category</th>
                <th className="px-3 py-4 font-semibold">Price</th>
                <th className="px-3 py-4 font-semibold">Stock</th>
                <th className="px-3 py-4 font-semibold">Status</th>
                <th className="px-6 py-4 text-right font-semibold">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {filteredProducts.length === 0 ? (
                <tr>
                  <td colSpan="6" className="py-12 text-center text-slate-400">
                    <div className="flex flex-col items-center justify-center">
                      <PackageOpen className="h-12 w-12 text-slate-600 mb-3" />
                      <p>No products found.</p>
                    </div>
                  </td>
                </tr>
              ) : filteredProducts.map((product) => (
                <tr key={product.id} className="hover:bg-slate-800/50 transition-colors">
                  <td className="py-4 pl-6 pr-3">
                    <div className="flex items-center gap-4">
                      <img 
                        src={mediaUrl(product.image)} 
                        alt={product.name} 
                        className="h-12 w-12 rounded-lg object-cover bg-slate-800"
                      />
                      <div>
                        <div className="font-medium text-slate-200">{product.name}</div>
                      </div>
                    </div>
                  </td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-slate-400">
                    {product.category_name}
                  </td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm font-medium text-slate-300">
                    {formatConvertedCurrency(product.price)}
                  </td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-slate-400">
                    {product.stock}
                  </td>
                  <td className="whitespace-nowrap px-3 py-4">
                    {product.stock === 0 ? (
                      <span className="inline-flex items-center rounded-full bg-red-500/10 px-2.5 py-0.5 text-xs font-medium text-red-400">
                        Out of Stock
                      </span>
                    ) : product.stock < 10 ? (
                      <span className="inline-flex items-center rounded-full bg-amber-500/10 px-2.5 py-0.5 text-xs font-medium text-amber-400">
                        Low Stock
                      </span>
                    ) : (
                      <span className="inline-flex items-center rounded-full bg-emerald-500/10 px-2.5 py-0.5 text-xs font-medium text-emerald-400">
                        In Stock
                      </span>
                    )}
                  </td>
                  <td className="py-4 pr-6 pl-3 text-right">
                    <div className="flex justify-end gap-2">
                      <button 
                        onClick={() => setSelectedProduct(product)}
                        className="p-2 text-slate-400 hover:text-indigo-400 transition-colors"
                        title="View Details"
                      >
                        <Eye className="h-4 w-4" />
                      </button>
                      <button className="p-2 text-slate-400 hover:text-indigo-400 transition-colors" title="Edit">
                        <Edit className="h-4 w-4" />
                      </button>
                      <button 
                        onClick={() => handleDelete(product.id)}
                        className="p-2 text-slate-400 hover:text-rose-400 transition-colors"
                        title="Delete"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {totalPages > 1 && (
        <div className="flex items-center justify-between mt-6 px-4">
          <button 
            disabled={currentPage === 1}
            onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
            className="rounded-lg border border-slate-700 bg-slate-800/50 px-4 py-2 text-sm font-medium text-slate-300 hover:bg-slate-800 disabled:opacity-50 transition-colors"
          >
            Previous
          </button>
          <span className="text-sm text-slate-400">Page {currentPage} of {totalPages}</span>
          <button 
            disabled={currentPage === totalPages}
            onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
            className="rounded-lg border border-slate-700 bg-slate-800/50 px-4 py-2 text-sm font-medium text-slate-300 hover:bg-slate-800 disabled:opacity-50 transition-colors"
          >
            Next
          </button>
        </div>
      )}

      {showAddModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
          <div className="w-full max-w-lg rounded-2xl border border-slate-800 bg-slate-900 p-6 shadow-2xl max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-slate-100">Add New Product</h2>
              <button 
                onClick={() => setShowAddModal(false)}
                className="text-slate-400 hover:text-slate-200 transition-colors"
              >
                <X className="h-5 w-5" />
              </button>
            </div>
            
            <form onSubmit={handleAddSubmit} className="space-y-4">
              <div>
                <label className="mb-2 block text-sm font-medium text-slate-300">Name</label>
                <input 
                  type="text" 
                  required
                  value={newProduct.name}
                  onChange={(e) => setNewProduct({...newProduct, name: e.target.value})}
                  className="w-full rounded-lg border border-slate-700 bg-slate-800/50 px-4 py-2 text-slate-200 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                  placeholder="Product name"
                />
              </div>
              
              <div>
                <label className="mb-2 block text-sm font-medium text-slate-300">Description</label>
                <textarea 
                  required
                  rows="3"
                  value={newProduct.description}
                  onChange={(e) => setNewProduct({...newProduct, description: e.target.value})}
                  className="w-full rounded-lg border border-slate-700 bg-slate-800/50 px-4 py-2 text-slate-200 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                  placeholder="Product description"
                ></textarea>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="mb-2 block text-sm font-medium text-slate-300">Price (INR)</label>
                  <input 
                    type="number" 
                    step="0.01"
                    required
                    value={newProduct.price}
                    onChange={(e) => setNewProduct({...newProduct, price: e.target.value})}
                    className="w-full rounded-lg border border-slate-700 bg-slate-800/50 px-4 py-2 text-slate-200 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                  />
                </div>
                <div>
                  <label className="mb-2 block text-sm font-medium text-slate-300">Stock</label>
                  <input 
                    type="number" 
                    required
                    value={newProduct.stock}
                    onChange={(e) => setNewProduct({...newProduct, stock: e.target.value})}
                    className="w-full rounded-lg border border-slate-700 bg-slate-800/50 px-4 py-2 text-slate-200 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                  />
                </div>
              </div>

              <div>
                <label className="mb-2 block text-sm font-medium text-slate-300">Category</label>
                <select 
                  required
                  value={newProduct.category}
                  onChange={(e) => setNewProduct({...newProduct, category: e.target.value})}
                  className="w-full rounded-lg border border-slate-700 bg-slate-800/50 px-4 py-2 text-slate-200 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                >
                  <option value="">Select a category</option>
                  {categories.map(c => (
                    <option key={c.id} value={c.id}>{c.name}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="mb-2 block text-sm font-medium text-slate-300">Image</label>
                <input 
                  type="file" 
                  required
                  accept="image/*"
                  onChange={(e) => setNewProduct({...newProduct, image: e.target.files[0]})}
                  className="w-full text-sm text-slate-400 file:mr-4 file:rounded-full file:border-0 file:bg-indigo-500/10 file:px-4 file:py-2 file:text-sm file:font-semibold file:text-indigo-400 hover:file:bg-indigo-500/20"
                />
              </div>

              <div className="mt-6 flex justify-end gap-3">
                <button 
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="rounded-lg px-4 py-2 text-sm font-medium text-slate-300 hover:bg-slate-800 transition-colors"
                >
                  Cancel
                </button>
                <button 
                  type="submit"
                  className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700 transition-colors"
                >
                  Add Product
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {selectedProduct && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
          <div className="w-full max-w-2xl rounded-2xl border border-slate-800 bg-slate-900 p-6 shadow-2xl overflow-hidden flex flex-col md:flex-row gap-6">
            <div className="md:w-1/2 flex-shrink-0">
              <img 
                src={mediaUrl(selectedProduct.image)} 
                alt={selectedProduct.name} 
                className="w-full h-auto rounded-xl object-cover bg-slate-800 border border-slate-800"
              />
            </div>
            <div className="md:w-1/2 flex flex-col">
              <div className="flex justify-between items-start mb-2">
                <h2 className="text-2xl font-bold text-slate-100">{selectedProduct.name}</h2>
                <button 
                  onClick={() => setSelectedProduct(null)}
                  className="text-slate-400 hover:text-slate-200 transition-colors"
                >
                  <X className="h-5 w-5" />
                </button>
              </div>
              <div className="mb-4 flex items-center gap-2">
                <span className="inline-block rounded-full bg-indigo-500/10 px-3 py-1 text-xs font-semibold text-indigo-400">
                  {selectedProduct.category_name}
                </span>
                {selectedProduct.stock === 0 ? (
                  <span className="inline-flex items-center rounded-full bg-red-500/10 px-2.5 py-0.5 text-xs font-semibold text-red-400">
                    Out of Stock
                  </span>
                ) : selectedProduct.stock < 10 ? (
                  <span className="inline-flex items-center rounded-full bg-amber-500/10 px-2.5 py-0.5 text-xs font-semibold text-amber-400">
                    Low Stock
                  </span>
                ) : (
                  <span className="inline-flex items-center rounded-full bg-emerald-500/10 px-2.5 py-0.5 text-xs font-semibold text-emerald-400">
                    In Stock
                  </span>
                )}
              </div>
              <p className="text-slate-400 mb-6 flex-1 text-sm leading-relaxed">
                {selectedProduct.description}
              </p>
              
              <div className="space-y-3 bg-slate-800/30 rounded-xl p-4 border border-slate-800/50">
                <div className="flex justify-between">
                  <span className="text-slate-400 text-sm">Price:</span>
                  <span className="text-slate-200 font-semibold">{formatConvertedCurrency(selectedProduct.price)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400 text-sm">Stock Available:</span>
                  <span className="text-slate-200 font-semibold">{selectedProduct.stock} units</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400 text-sm">Added On:</span>
                  <span className="text-slate-200 font-semibold">{new Date(selectedProduct.created_at).toLocaleDateString()}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
"""

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated AdminProducts.jsx")
