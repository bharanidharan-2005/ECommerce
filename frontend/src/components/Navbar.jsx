import React, { useState, useEffect, useRef } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import api from "../api/axios";
import { useDispatch, useSelector } from "react-redux";
import { setCurrency } from "../features/ui/uiSlice";
import { FiSearch, FiShoppingCart, FiUser, FiHeart, FiX, FiMenu, FiChevronDown, FiLogOut, FiSettings } from "react-icons/fi";
import { motion, AnimatePresence } from "framer-motion";

import { logout } from "../features/auth/authSlice";
import { openCart } from "../features/ui/uiSlice";
import { selectCartCount } from "../features/cart/cartSlice";
import { selectWishlistItems } from "../features/products/wishlistSlice";

const currencies = [
  { code: "INR", symbol: "₹" },
  { code: "USD", symbol: "$" },
  { code: "EUR", symbol: "€" },
  { code: "GBP", symbol: "£" }
];

export default function Navbar() {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [isSearchLoading, setIsSearchLoading] = useState(false);
  const searchRef = useRef(null);
  
  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      if (searchQuery.trim().length >= 2) {
        setIsSearchLoading(true);
        api.get(`/products/?search=${searchQuery}&limit=5`)
          .then(res => {
            setSearchResults(res.data?.results || res.data || []);
          })
          .catch(err => console.error(err))
          .finally(() => setIsSearchLoading(false));
      } else {
        setSearchResults([]);
      }
    }, 500);

    return () => clearTimeout(delayDebounceFn);
  }, [searchQuery]);

  const [isAccountOpen, setIsAccountOpen] = useState(false);
  const [isCurrencyOpen, setIsCurrencyOpen] = useState(false);
  const currentCurrency = useSelector((state) => state.ui.currency);
  const selectedCurrency = currencies.find(c => c.code === currentCurrency) || currencies[0];
  
  const [categories, setCategories] = useState([]);
  const [isCategoriesMegaMenuOpen, setIsCategoriesMegaMenuOpen] = useState(false);
  const [isMobileCategoriesOpen, setIsMobileCategoriesOpen] = useState(false);
  const location = useLocation();
  
  const accountRef = useRef(null);
  const currencyRef = useRef(null);
  
  const dispatch = useDispatch();
  const navigate = useNavigate();
  
  const count = useSelector(selectCartCount);
  const { user } = useSelector((state) => state.auth);
  const wishlistItems = useSelector(selectWishlistItems);

  useEffect(() => {
    api.get("/products/categories/")
      .then(res => {
        const data = res.data?.results || res.data;
        if (Array.isArray(data)) setCategories(data);
      })
      .catch(err => console.error("Error fetching categories:", err));
  }, []);

  useEffect(() => {
    const handleScroll = () => setIsScrolled(window.scrollY > 20);
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (accountRef.current && !accountRef.current.contains(event.target)) {
        setIsAccountOpen(false);
      }
      if (currencyRef.current && !currencyRef.current.contains(event.target)) {
        setIsCurrencyOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/products?search=${encodeURIComponent(searchQuery.trim())}`);
      setIsSearchOpen(false);
      setSearchQuery("");
      setIsMobileMenuOpen(false);
    }
  };

  const searchParams = new URLSearchParams(location.search);
  const categoryParam = searchParams.get('category');
  const currentCategoryLabel = categoryParam && categoryParam !== 'all'
    ? categories.find(c => c.name.toLowerCase() === categoryParam.toLowerCase() || (c.link && c.link.includes(categoryParam)))?.name || (categoryParam.charAt(0).toUpperCase() + categoryParam.slice(1).replace('-', ' '))
    : 'Categories';

  return (
    <header
      className={`fixed top-0 z-50 w-full transition-all duration-300 ${
        isScrolled ? "bg-[#0B1020]/95 backdrop-blur-md shadow-lg shadow-black/20 border-b border-white/5" : "bg-transparent border-b border-transparent"
      }`}
    >
      <nav className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
        
        {/* Mobile Left: Hamburger */}
        <div className="flex items-center lg:hidden gap-3">
          <button
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            className="text-slate-300 transition hover:text-white"
            aria-label="Toggle menu"
          >
            {isMobileMenuOpen ? <FiX size={24} /> : <FiMenu size={24} />}
          </button>
          <button
            onClick={() => setIsSearchOpen(!isSearchOpen)}
            className="text-slate-300 transition hover:text-white"
            aria-label="Search"
          >
            <FiSearch size={20} />
          </button>
        </div>

        {/* Logo */}
        <Link to="/" className="flex items-center gap-2 group">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-indigo-600 text-white transition-transform group-hover:scale-105 group-hover:rotate-3 shadow-lg shadow-indigo-600/20">
            <span className="font-black text-xl leading-none tracking-tighter">S</span>
          </div>
          <span className="text-xl font-bold tracking-tight text-white hidden sm:block">
            Shop<span className="text-indigo-400">Verse</span>
          </span>
        </Link>

        {/* Desktop Center: Navigation */}
        <div className="hidden lg:flex items-center gap-8 text-sm font-semibold text-slate-300">
          <Link 
            to="/products" 
            className={`transition py-2 ${location.pathname === '/products' && !location.search ? 'text-indigo-400 font-bold' : 'hover:text-indigo-400'}`}
          >
            Shop
          </Link>
          
          <div 
            className="relative py-2"
            onMouseEnter={() => setIsCategoriesMegaMenuOpen(true)}
            onMouseLeave={() => setIsCategoriesMegaMenuOpen(false)}
          >
            <button 
              className={`transition flex items-center gap-1 ${location.search.includes('category=') ? 'text-indigo-400 font-bold' : 'hover:text-indigo-400'}`}
            >
              {currentCategoryLabel} <FiChevronDown size={14} className={`transition-transform ${isCategoriesMegaMenuOpen ? 'rotate-180' : ''}`} />
            </button>
            
            <AnimatePresence>
              {isCategoriesMegaMenuOpen && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 10 }}
                  transition={{ duration: 0.15 }}
                  className="absolute left-1/2 -translate-x-1/2 top-full pt-2 w-48"
                >
                  <div className="rounded-xl border border-slate-700 bg-slate-800 p-2 shadow-xl shadow-slate-900/50 flex flex-col gap-1">
                    <Link
                      to="/products?category=all"
                      className="px-3 py-2 rounded-lg text-slate-300 hover:bg-slate-700 hover:text-white transition"
                      onClick={() => setIsCategoriesMegaMenuOpen(false)}
                    >
                      All Categories
                    </Link>
                    {categories.map(cat => (
                      <Link
                        key={cat.id}
                        to={`/products?category=${encodeURIComponent(cat.name)}`}
                        className="px-3 py-2 rounded-lg text-slate-300 hover:bg-slate-700 hover:text-white transition"
                        onClick={() => setIsCategoriesMegaMenuOpen(false)}
                      >
                        {cat.name}
                      </Link>
                    ))}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          <Link 
            to="/products?sort=-created_at" 
            className={`transition py-2 ${location.search.includes('sort=-created_at') ? 'text-indigo-400 font-bold' : 'hover:text-indigo-400'}`}
          >
            New Arrivals
          </Link>
          <Link 
            to="/products?sale=true" 
            className={`transition py-2 ${location.search.includes('sale=true') ? 'text-indigo-400 font-bold' : 'hover:text-indigo-400'}`}
          >
            Deals
          </Link>
        </div>

        {/* Right: Actions */}
        <div className="flex items-center gap-4 sm:gap-5">
          {/* Search (Desktop) */}
          <button
            onClick={() => setIsSearchOpen(!isSearchOpen)}
            className="hidden lg:block p-2 text-slate-300 transition hover:text-indigo-400"
            aria-label="Search"
          >
            <FiSearch size={20} />
          </button>

          {/* Wishlist */}
          <Link
            to="/wishlist"
            className="hidden sm:flex relative p-2 text-slate-300 transition hover:text-indigo-400"
            aria-label="Wishlist"
          >
            <FiHeart size={20} />
            {wishlistItems?.length > 0 && (
              <span className="absolute top-1 right-0 flex h-4 min-w-[16px] items-center justify-center rounded-full bg-indigo-500 px-1 text-[10px] font-bold text-white shadow-sm shadow-indigo-900/50">
                {wishlistItems.length}
              </span>
            )}
          </Link>

          {/* Cart */}
          <button
            onClick={() => dispatch(openCart())}
            className="relative p-2 text-slate-300 transition hover:text-indigo-400"
            aria-label={`Open cart (${count} items)`}
          >
            <FiShoppingCart size={20} />
            {count > 0 && (
              <span className="absolute top-0 -right-1 flex h-5 min-w-[20px] items-center justify-center rounded-full bg-indigo-500 px-1 text-[11px] font-bold text-white shadow-sm shadow-indigo-900/50 ring-2 ring-slate-900">
                {count}
              </span>
            )}
          </button>

          {/* Currency Selector */}
          <div className="hidden sm:block relative border-l border-slate-700 pl-4" ref={currencyRef}>
            <button
              onClick={() => setIsCurrencyOpen(!isCurrencyOpen)}
              className="flex items-center gap-1.5 text-sm font-semibold text-slate-300 hover:text-white transition"
            >
              <span>{selectedCurrency.code} {selectedCurrency.symbol}</span>
              <FiChevronDown size={14} className={`text-slate-500 transition-transform ${isCurrencyOpen ? "rotate-180" : ""}`} />
            </button>
            <AnimatePresence>
              {isCurrencyOpen && (
                <motion.div
                  initial={{ opacity: 0, y: 10, scale: 0.95 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  exit={{ opacity: 0, y: 10, scale: 0.95 }}
                  transition={{ duration: 0.15 }}
                  className="absolute right-0 top-full mt-3 w-28 rounded-xl border border-slate-700 bg-slate-800 py-1 shadow-xl shadow-slate-900/50 overflow-hidden"
                >
                  {currencies.map(c => (
                    <button
                      key={c.code}
                      onClick={() => { dispatch(setCurrency(c.code)); setIsCurrencyOpen(false); }}
                      className={`flex w-full items-center justify-between px-4 py-2 text-sm transition ${selectedCurrency.code === c.code ? 'bg-slate-700 text-white font-bold' : 'text-slate-300 hover:bg-slate-700/50 hover:text-white'}`}
                    >
                      <span>{c.code}</span>
                      <span>{c.symbol}</span>
                    </button>
                  ))}
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Account Dropdown */}
          <div className="relative ml-1 hidden sm:block" ref={accountRef}>
            {user ? (
              <button
                onClick={() => setIsAccountOpen(!isAccountOpen)}
                className="flex items-center gap-2 rounded-full border border-slate-700 bg-slate-800/50 py-1.5 pl-2 pr-3 text-sm font-medium text-slate-200 transition hover:bg-slate-700 hover:border-slate-600"
              >
                <div className="flex h-6 w-6 items-center justify-center rounded-full bg-indigo-600 text-white shadow-inner">
                  <FiUser size={14} />
                </div>
                <span className="hidden lg:inline max-w-[100px] truncate">{user.username || 'Account'}</span>
                <FiChevronDown size={14} className={`text-slate-400 transition-transform ${isAccountOpen ? "rotate-180" : ""}`} />
              </button>
            ) : (
              <button onClick={() => navigate("/login")} className="flex items-center gap-2 text-sm font-semibold text-slate-300 hover:text-white transition">
                <FiUser size={18} />
                <span className="hidden lg:inline">Sign In</span>
              </button>
            )}

            {/* Account Menu */}
            <AnimatePresence>
              {isAccountOpen && user && (
                <motion.div
                  initial={{ opacity: 0, y: 10, scale: 0.95 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  exit={{ opacity: 0, y: 10, scale: 0.95 }}
                  transition={{ duration: 0.15 }}
                  className="absolute right-0 top-full mt-3 w-56 rounded-xl border border-slate-700 bg-slate-800 py-2 shadow-xl shadow-slate-900/50"
                >
                  <div className="border-b border-slate-700/50 px-4 py-3 text-sm">
                    <p className="font-bold text-white">{user.username}</p>
                    <p className="truncate text-slate-400 text-xs mt-0.5">{user.email || 'shopverse@gmail.com'}</p>
                  </div>
                  <div className="py-2">
                    <Link to="/profile?tab=account" className="flex items-center gap-3 px-4 py-2.5 text-sm font-medium text-slate-300 hover:bg-slate-700 hover:text-white transition">
                      <FiUser size={16} className="text-slate-400" /> My Account
                    </Link>
                    <Link to="/profile?tab=orders" className="flex items-center gap-3 px-4 py-2.5 text-sm font-medium text-slate-300 hover:bg-slate-700 hover:text-white transition">
                      <FiShoppingCart size={16} className="text-slate-400" /> My Orders
                    </Link>
                    <Link to="/wishlist" className="flex items-center gap-3 px-4 py-2.5 text-sm font-medium text-slate-300 hover:bg-slate-700 hover:text-white transition sm:hidden">
                      <FiHeart size={16} className="text-slate-400" /> Wishlist
                    </Link>
                    {user.is_staff && (
                      <Link to="/admin" className="flex items-center gap-3 px-4 py-2.5 text-sm font-bold text-indigo-400 hover:bg-slate-700 hover:text-indigo-300 transition">
                        <FiSettings size={16} /> Admin Panel
                      </Link>
                    )}
                  </div>
                  <div className="border-t border-slate-700/50 py-2">
                    <button
                      onClick={() => {
                        dispatch(logout());
                        navigate("/");
                      }}
                      className="flex w-full items-center gap-3 px-4 py-2.5 text-sm font-medium text-rose-400 hover:bg-rose-500/10 hover:text-rose-300 transition"
                    >
                      <FiLogOut size={16} /> Logout
                    </button>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </nav>

      {/* Search Overlay */}
              <AnimatePresence>
          {isSearchOpen && (
            <motion.div
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="absolute left-0 top-0 z-50 flex h-full w-full items-center bg-slate-900/95 backdrop-blur px-4 sm:px-6"
            >
              <div className="w-full max-w-4xl mx-auto relative" ref={searchRef}>
                <form onSubmit={handleSearchSubmit} className="flex w-full items-center gap-4 relative z-10">
                  <FiSearch size={22} className="text-indigo-400" />
                  <input
                    type="text"
                    autoFocus
                    placeholder="Search products, categories and more..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="flex-1 bg-transparent text-lg text-white placeholder-slate-500 focus:outline-none"
                  />
                  {isSearchLoading && (
                    <div className="w-5 h-5 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
                  )}
                  <button
                    type="button"
                    onClick={() => {
                      setIsSearchOpen(false);
                      setSearchResults([]);
                    }}
                    className="rounded-full p-2 text-slate-400 hover:bg-slate-800 hover:text-white transition"
                  >
                    <FiX size={24} />
                  </button>
                </form>

                {searchResults.length > 0 && searchQuery.trim().length >= 2 && (
                  <div className="absolute top-full left-0 w-full mt-4 bg-slate-800 border border-slate-700 rounded-2xl overflow-hidden shadow-2xl z-50">
                    {searchResults.map((product) => (
                      <Link 
                        key={product.id}
                        to={/products/}
                        onClick={() => {
                          setIsSearchOpen(false);
                          setSearchResults([]);
                          setSearchQuery("");
                        }}
                        className="flex items-center gap-4 p-4 hover:bg-slate-700 transition"
                      >
                        <div className="h-12 w-12 rounded-lg bg-slate-900 overflow-hidden shrink-0">
                          {product.image && <img src={product.image} alt={product.name} className="w-full h-full object-cover" />}
                        </div>
                        <div className="flex-1 min-w-0">
                          <h4 className="text-sm font-bold text-slate-200 truncate">{product.name}</h4>
                          <p className="text-xs text-slate-400 truncate">{product.category?.name}</p>
                        </div>
                        <div className="font-bold text-sm text-indigo-400">
                          
                        </div>
                      </Link>
                    ))}
                    <button 
                      onClick={handleSearchSubmit}
                      className="w-full p-3 text-center text-sm font-bold text-indigo-400 bg-slate-800/50 hover:bg-slate-700 transition border-t border-slate-700"
                    >
                      View all results
                    </button>
                  </div>
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>

      {/* Mobile Menu */}
      <AnimatePresence>
        {isMobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="lg:hidden border-t border-slate-800 bg-slate-900 overflow-hidden"
          >
            <div className="flex flex-col px-4 py-4 space-y-1 font-semibold text-slate-300">
              <Link to="/products" className={`py-3 px-2 rounded-lg transition ${location.pathname === '/products' && !location.search ? 'bg-indigo-600/20 text-indigo-400' : 'hover:bg-slate-800 hover:text-white'}`} onClick={() => setIsMobileMenuOpen(false)}>Shop</Link>
              
              <div className="flex flex-col">
                <div 
                  className={`flex items-center justify-between py-3 px-2 rounded-lg transition cursor-pointer ${location.search.includes('category=') ? 'bg-indigo-600/20 text-indigo-400' : 'hover:bg-slate-800 hover:text-white'}`}
                  onClick={() => setIsMobileCategoriesOpen(!isMobileCategoriesOpen)}
                >
                  <span>{currentCategoryLabel}</span>
                  <FiChevronDown size={18} className={`transition-transform ${isMobileCategoriesOpen ? 'rotate-180' : ''}`} />
                </div>
                
                <AnimatePresence>
                  {isMobileCategoriesOpen && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: 'auto', opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      className="overflow-hidden pl-4 pr-2"
                    >
                      <div className="py-2 flex flex-col space-y-1 border-l-2 border-slate-700 ml-2">
                        <Link 
                          to="/products?category=all" 
                          className="py-2 pl-4 text-sm text-slate-400 hover:text-white transition"
                          onClick={() => setIsMobileMenuOpen(false)}
                        >
                          All Categories
                        </Link>
                        {categories.map(cat => (
                          <Link 
                            key={cat.id}
                            to={`/products?category=${encodeURIComponent(cat.name)}`} 
                            className="py-2 pl-4 text-sm text-slate-400 hover:text-white transition"
                            onClick={() => setIsMobileMenuOpen(false)}
                          >
                            {cat.name}
                          </Link>
                        ))}
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>

              <Link to="/products?sort=-created_at" className={`py-3 px-2 rounded-lg transition ${location.search.includes('sort=-created_at') ? 'bg-indigo-600/20 text-indigo-400' : 'hover:bg-slate-800 hover:text-white'}`} onClick={() => setIsMobileMenuOpen(false)}>New Arrivals</Link>
              <Link to="/products?sale=true" className={`py-3 px-2 rounded-lg transition ${location.search.includes('sale=true') ? 'bg-indigo-600/20 text-indigo-400' : 'hover:bg-slate-800 hover:text-white'}`} onClick={() => setIsMobileMenuOpen(false)}>Deals</Link>
              
              <div className="my-4 border-t border-slate-800" />
              
              {/* Mobile Account Options */}
              {user ? (
                <>
                  <Link to="/profile?tab=account" className="flex items-center gap-3 py-3 px-2 rounded-lg hover:bg-slate-800 hover:text-white transition" onClick={() => setIsMobileMenuOpen(false)}>
                    <FiUser size={18} className="text-slate-400" /> My Account
                  </Link>
                  <Link to="/wishlist" className="flex items-center gap-3 py-3 px-2 rounded-lg hover:bg-slate-800 hover:text-white transition" onClick={() => setIsMobileMenuOpen(false)}>
                    <FiHeart size={18} className="text-slate-400" /> Wishlist
                  </Link>
                  <button onClick={() => { dispatch(logout()); setIsMobileMenuOpen(false); }} className="flex items-center gap-3 py-3 px-2 rounded-lg text-rose-400 hover:bg-slate-800 transition text-left">
                    <FiLogOut size={18} /> Logout
                  </button>
                </>
              ) : (
                <Link to="/login" className="flex items-center gap-3 py-3 px-2 rounded-lg hover:bg-slate-800 hover:text-white transition" onClick={() => setIsMobileMenuOpen(false)}>
                  <FiUser size={18} className="text-slate-400" /> Sign In
                </Link>
              )}

              {/* Mobile Currency Selector */}
              <div className="py-3 px-2 mt-4 flex items-center justify-between border-t border-slate-800">
                <span className="text-sm text-slate-400 font-medium">Currency</span>
                <div className="flex gap-2">
                  {currencies.map(c => (
                    <button
                      key={c.code}
                      onClick={() => dispatch(setCurrency(c.code))}
                      className={`px-3 py-1.5 rounded-lg text-xs font-bold transition ${selectedCurrency.code === c.code ? 'bg-indigo-600 text-white' : 'bg-slate-800 text-slate-400 hover:bg-slate-700'}`}
                    >
                      {c.symbol}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  );
}
