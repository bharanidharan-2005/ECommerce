import fs from 'fs';

const navbarContent = \import React, { useState, useEffect, useRef } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { FiSearch, FiShoppingCart, FiUser, FiHeart, FiX, FiMenu, FiChevronDown, FiLogOut, FiSettings } from "react-icons/fi";
import { motion, AnimatePresence } from "framer-motion";
import { openCart } from "../features/cart/cartSlice";
import { logout } from "../features/auth/authSlice";
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
  const [isAccountOpen, setIsAccountOpen] = useState(false);
  const [isCurrencyOpen, setIsCurrencyOpen] = useState(false);
  const [selectedCurrency, setSelectedCurrency] = useState(currencies[0]);
  
  const accountRef = useRef(null);
  const currencyRef = useRef(null);
  
  const dispatch = useDispatch();
  const navigate = useNavigate();
  
  const count = useSelector((state) => state.cart.count);
  const { user } = useSelector((state) => state.auth);
  const wishlistItems = useSelector(selectWishlistItems);

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
      navigate(\/products?search=\\);
      setIsSearchOpen(false);
      setSearchQuery("");
      setIsMobileMenuOpen(false);
    }
  };

  return (
    <header
      className={\ixed top-0 z-50 w-full transition-all duration-300 \\}
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
          <Link to="/products" className="transition hover:text-indigo-400 py-2">Shop</Link>
          <Link to="/products?category=all" className="transition hover:text-indigo-400 py-2">Categories</Link>
          <Link to="/products?sort=-created_at" className="transition hover:text-indigo-400 py-2">New Arrivals</Link>
          <Link to="/products?sale=true" className="transition hover:text-indigo-400 py-2">Deals</Link>
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
            aria-label={\Open cart (\ items)\}
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
              <FiChevronDown size={14} className={\	ext-slate-500 transition-transform \\} />
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
                      onClick={() => { setSelectedCurrency(c); setIsCurrencyOpen(false); }}
                      className={\lex w-full items-center justify-between px-4 py-2 text-sm transition \\}
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
                <FiChevronDown size={14} className={\	ext-slate-400 transition-transform \\} />
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
                    <Link to="/profile" className="flex items-center gap-3 px-4 py-2.5 text-sm font-medium text-slate-300 hover:bg-slate-700 hover:text-white transition">
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
            <form onSubmit={handleSearchSubmit} className="flex w-full max-w-4xl mx-auto items-center gap-4">
              <FiSearch size={22} className="text-indigo-400" />
              <input
                type="text"
                autoFocus
                placeholder="Search products, categories and more..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="flex-1 bg-transparent text-lg text-white placeholder-slate-500 focus:outline-none"
              />
              <button
                type="button"
                onClick={() => setIsSearchOpen(false)}
                className="rounded-full p-2 text-slate-400 hover:bg-slate-800 hover:text-white transition"
              >
                <FiX size={24} />
              </button>
            </form>
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
              <Link to="/products" className="py-3 px-2 rounded-lg hover:bg-slate-800 hover:text-white transition" onClick={() => setIsMobileMenuOpen(false)}>Shop</Link>
              <Link to="/products?category=all" className="py-3 px-2 rounded-lg hover:bg-slate-800 hover:text-white transition" onClick={() => setIsMobileMenuOpen(false)}>Categories</Link>
              <Link to="/products?sort=-created_at" className="py-3 px-2 rounded-lg hover:bg-slate-800 hover:text-white transition" onClick={() => setIsMobileMenuOpen(false)}>New Arrivals</Link>
              <Link to="/products?sale=true" className="py-3 px-2 rounded-lg hover:bg-slate-800 hover:text-white transition" onClick={() => setIsMobileMenuOpen(false)}>Deals</Link>
              
              <div className="my-4 border-t border-slate-800" />
              
              {/* Mobile Account Options */}
              {user ? (
                <>
                  <Link to="/profile" className="flex items-center gap-3 py-3 px-2 rounded-lg hover:bg-slate-800 hover:text-white transition" onClick={() => setIsMobileMenuOpen(false)}>
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
                      onClick={() => setSelectedCurrency(c)}
                      className={\px-3 py-1.5 rounded-lg text-xs font-bold transition \\}
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
}\;

fs.writeFileSync('src/components/Navbar.jsx', navbarContent);
