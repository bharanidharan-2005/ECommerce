import { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { FiSearch, FiX, FiFilter, FiChevronDown } from "react-icons/fi";
import { motion, AnimatePresence } from "framer-motion";
import { useSearchParams } from "react-router-dom";

import BentoProductCard from "../components/BentoProductCard.jsx";
import EmptyState from "../components/ui/EmptyState.jsx";
import ErrorState from "../components/ui/ErrorState.jsx";
import Pagination from "../components/Pagination.jsx";
import SkeletonCard from "../components/SkeletonCard.jsx";
import PageTransition from "../components/PageTransition.jsx";
import api from "../api/axios";
import { fetchProducts } from "../features/products/productsSlice";

const bentoVariantFor = (i) => (i % 6 === 0 ? "featured" : i % 6 === 3 ? "wide" : "default");

export default function ProductListPage() {
  const dispatch = useDispatch();
  const { items, pages, loading, error } = useSelector((s) => s.products);

  const [searchParams, setSearchParams] = useSearchParams();
  const [search, setSearch] = useState(searchParams.get("search") || "");
  const [category, setCategory] = useState(searchParams.get("category") && searchParams.get("category") !== "all" ? searchParams.get("category") : "");
  const [ordering, setOrdering] = useState(searchParams.get("sort") || (searchParams.get("sale") === "true" ? "price" : ""));


  const [minPrice, setMinPrice] = useState(searchParams.get("minPrice") || "");
  const [maxPrice, setMaxPrice] = useState(searchParams.get("maxPrice") || "");
  const [inStock, setInStock] = useState(searchParams.get("inStock") === "true");
  const isSale = searchParams.get("sale") === "true";
  const [page, setPage] = useState(1);
  const [showFilters, setShowFilters] = useState(false);
  const [categoriesList, setCategoriesList] = useState([{ id: "", name: "All Collections" }]);

  useEffect(() => {
    const urlSearch = searchParams.get("search") || "";
    const urlSort = searchParams.get("sort");
    const urlSale = searchParams.get("sale");
    const urlCategory = searchParams.get("category");

    setSearch(urlSearch);

    if (urlSort) {
      setOrdering(urlSort);
    } else if (urlSale === "true") {
      setOrdering("price");
    } else {
      setOrdering("");
    }

    if (urlCategory && categoriesList.length > 1) {
      if (urlCategory === "all") {
        setCategory("");
      } else {
        const matched = categoriesList.find(c => c.name.toLowerCase() === urlCategory.toLowerCase() || (c.slug && c.slug.toLowerCase() === urlCategory.toLowerCase()) || String(c.id) === urlCategory);
        if (matched) {
          setCategory(matched.id);
        } else {
          setCategory("");
        }
      }
    } else if (!urlCategory) {
      setCategory("");
    }
  }, [searchParams, categoriesList]);

  useEffect(() => {
    const fetchCats = async () => {
      try {
        const res = await api.get("/products/categories/");
        const cats = res.data.results || res.data;
        setCategoriesList([
          { id: "", name: "All Collections" },
          ...cats.map(c => ({ id: String(c.id), name: c.name, slug: c.slug }))
        ]);
      } catch (err) {
        console.error("Failed to fetch categories");
      }
    };
    fetchCats();
  }, []);

  useEffect(() => {
    const t = setTimeout(() => {
      dispatch(fetchProducts({ page, search, category, ordering, min_price: minPrice, max_price: maxPrice, in_stock: inStock, sale: isSale }));
    }, 350);
    return () => clearTimeout(t);
  }, [dispatch, page, search, category, ordering, minPrice, maxPrice, inStock, isSale]);


  // Sync state back to URL
  useEffect(() => {
    const params = new URLSearchParams(searchParams);
    if (search) params.set("search", search); else params.delete("search");
    if (category) {
      const catObj = categoriesList.find(c => c.id === category);
      if (catObj && catObj.slug) params.set("category", catObj.slug);
      else params.set("category", category);
    } else {
      params.delete("category");
    }
    if (ordering) params.set("sort", ordering); else params.delete("sort");
    if (minPrice) params.set("minPrice", minPrice); else params.delete("minPrice");
    if (maxPrice) params.set("maxPrice", maxPrice); else params.delete("maxPrice");
    if (inStock) params.set("inStock", "true"); else params.delete("inStock");
    
    setSearchParams(params, { replace: true });
  }, [search, category, ordering, minPrice, maxPrice, inStock]);

  const hasFilters = search || category || ordering || minPrice || maxPrice || inStock;


  const resetAnd = (setter) => (value) => {
    setter(value);
    setPage(1);
  };

  const handleCategoryChange = (c) => {
    setCategory(c.id);
    setPage(1);
    const params = new URLSearchParams(searchParams);
    if (!c.id) {
      params.delete('category');
    } else {
      params.set('category', c.slug || c.name);
    }
    setSearchParams(params);
  };



  const SORTS = [
    { id: "", name: "Latest Arrivals" },
    { id: "-created_at", name: "Oldest First" },
    { id: "price", name: "Price: Low to High" },
    { id: "-price", name: "Price: High to Low" }
  ];

  return (
    <PageTransition>
      <div className="mx-auto max-w-[1400px] px-4 pt-40 pb-10 sm:px-6">
        {/* Header Section */}
        <div className="mb-10 text-center sm:text-left sm:flex sm:items-end sm:justify-between">
          <div>
            <h1 className="text-4xl font-black tracking-tight sm:text-5xl text-slate-100 mb-2">The Collection</h1>
            <p className="text-slate-400 text-lg">
              {loading ? "Curating our finest pieces..." : `Showing ${items.length} extraordinary items`}
            </p>
          </div>
          <div className="mt-6 sm:mt-0">
            <button 
              onClick={() => setShowFilters(!showFilters)}
              className={`flex items-center gap-2 px-5 py-2.5 rounded-full font-medium transition-all ${showFilters ? 'bg-indigo-500 text-white shadow-lg shadow-indigo-500/20' : 'bg-slate-800 text-slate-300 hover:bg-slate-700'}`}
            >
              <FiFilter /> {showFilters ? 'Hide Filters' : 'Show Filters'}
              {hasFilters && <span className="flex h-5 w-5 items-center justify-center rounded-full bg-indigo-400/20 text-xs text-indigo-300 ml-1">!</span>}
            </button>
          </div>
        </div>

        <div className="flex flex-col lg:flex-row gap-8">
          {/* Collapsible Sidebar */}
          <AnimatePresence>
            {showFilters && (
              <motion.div 
                initial={{ opacity: 0, width: 0, marginLeft: 0 }}
                animate={{ opacity: 1, width: "auto", marginLeft: 0 }}
                exit={{ opacity: 0, width: 0, overflow: 'hidden' }}
                className="w-full lg:w-72 shrink-0 space-y-6"
              >
                <div className="bg-slate-900/50 rounded-2xl border border-slate-800 p-6 sticky top-24">
                  <div className="flex items-center justify-between mb-6">
                    <h3 className="text-lg font-bold text-slate-200">Refine Search</h3>
                    {hasFilters && (
                      <button onClick={() => { setSearch(""); setCategory(""); setOrdering(""); setMinPrice(""); setMaxPrice(""); setInStock(false); setPage(1); }} className="text-xs font-semibold text-indigo-400 hover:text-indigo-300 uppercase tracking-wider">Clear All</button>
                    )}
                  </div>
                  
                  {/* Search */}
                  <div className="mb-6 relative">
                    <FiSearch className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500" />
                    <input 
                      value={search} onChange={(e) => resetAnd(setSearch)(e.target.value)}
                      placeholder="Search products..."
                      className="w-full bg-slate-800 border-slate-700 rounded-xl pl-11 pr-4 py-3 text-sm focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all text-slate-200 placeholder-slate-500" 
                    />
                  </div>

                  {/* Categories */}
                  <div className="mb-6">
                    <h4 className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-3">Categories</h4>
                    <div className="space-y-2">
                      {categoriesList.map(c => (
                        <label key={c.id} className="flex items-center gap-3 cursor-pointer group">
                          <div className={`w-5 h-5 rounded border flex items-center justify-center transition-colors ${category === c.id ? 'bg-indigo-500 border-indigo-500' : 'bg-slate-800 border-slate-600 group-hover:border-slate-500'}`}>
                            {category === c.id && <FiX size={12} className="text-white rotate-45" />}
                          </div>
                          <span className={`text-sm font-medium ${category === c.id ? 'text-indigo-400' : 'text-slate-300 group-hover:text-slate-200'}`}>{c.name}</span>
                          <input type="radio" className="sr-only" checked={category === c.id} onChange={() => handleCategoryChange(c)} />
                        </label>
                      ))}
                    </div>
                  </div>

                  {/* Sort */}
                  <div>
                    <h4 className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-3">Sort By</h4>
                    <div className="relative">
                      <select 
                        value={ordering} onChange={(e) => resetAnd(setOrdering)(e.target.value)}
                        className="w-full bg-slate-800 border-slate-700 rounded-xl px-4 py-3 text-sm appearance-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 text-slate-200"
                      >
                        {SORTS.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
                      </select>
                      <FiChevronDown className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-500 pointer-events-none" />
                    </div>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Main Grid */}
          <div className="flex-1 min-w-0">
            {error && <div className="mb-6"><ErrorState message={error} onRetry={() => dispatch(fetchProducts({ page, search, category, ordering, min_price: minPrice, max_price: maxPrice, in_stock: inStock, sale: isSale }))} /></div>}
            
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:gap-5">
              {loading
                ? [...Array(6)].map((_, i) => <SkeletonCard key={i} variant={bentoVariantFor(i)} />)
                : items.map((p, i) => <BentoProductCard key={p.id} product={p} variant={bentoVariantFor(i)} index={i} />)}
            </div>

            {!loading && !error && items.length === 0 && isSale && (
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
            )}

            {!loading && <div className="mt-12"><Pagination page={page} pages={pages} onPage={setPage} /></div>}
          </div>
        </div>
      </div>
    </PageTransition>
  );
}
