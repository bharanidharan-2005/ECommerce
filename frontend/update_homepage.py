import os

filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\HomePage.jsx"

content = """import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { motion, AnimatePresence } from "framer-motion";
import { FiArrowRight, FiShield, FiTruck, FiRefreshCw, FiHeadphones, FiCheck } from "react-icons/fi";

import BentoProductCard from "../components/BentoProductCard.jsx";
import SkeletonCard from "../components/SkeletonCard.jsx";
import PageTransition from "../components/PageTransition.jsx";
import { fetchProducts } from "../features/products/productsSlice";

const riseIn = (delay) => ({
  initial: { opacity: 0, y: 24 },
  whileInView: { opacity: 1, y: 0 },
  viewport: { once: true, margin: "-40px" },
  transition: { duration: 0.55, delay, ease: [0.22, 1, 0.36, 1] },
});

const mediaUrl = (path) => {
  if (!path) return "";
  if (/^https?:\/\//i.test(path)) return path;
  const base = (import.meta.env.VITE_API_URL || "http://localhost:8010/api").replace(/\/api$/, "");
  return `${base}${path}`;
};

export default function HomePage() {
  const dispatch = useDispatch();
  const { items, loading } = useSelector((s) => s.products);
  
  const [activeCategory, setActiveCategory] = useState("All");
  const [email, setEmail] = useState("");
  const [isSubscribed, setIsSubscribed] = useState(false);

  useEffect(() => {
    dispatch(fetchProducts({ page: 1, limit: 20 }));
  }, [dispatch]);

  // Derive available categories dynamically from fetched products
  const availableCategories = Array.from(new Set(items.map(p => p.category_name).filter(Boolean)));
  const categoryTabs = ["All", ...availableCategories.slice(0, 4)]; // Limit to 4 specific + All

  const filteredNewArrivals = items
    .filter(p => activeCategory === "All" || p.category_name === activeCategory)
    .slice(0, 8); // 2 rows of 4

  const bestSellers = [...items].sort((a, b) => (b.reviews?.length || 0) - (a.reviews?.length || 0)).slice(0, 4);
  const featuredProduct = items.find(p => p.category_name?.toLowerCase().includes('electronic')) || items[0];

  const handleSubscribe = (e) => {
    e.preventDefault();
    if(email) {
      setIsSubscribed(true);
      setEmail("");
      setTimeout(() => setIsSubscribed(false), 3000);
    }
  };

  return (
    <PageTransition>
      {/* ================= Hero Section ================= */}
      <section className="relative overflow-hidden bg-slate-900 pt-16 pb-20 sm:pt-24 sm:pb-32 lg:pb-36 border-b border-slate-800">
        <div aria-hidden className="absolute -left-24 -top-24 h-72 w-72 rounded-full bg-indigo-600/10 blur-3xl" />
        <div aria-hidden className="absolute bottom-0 right-0 h-96 w-96 rounded-full bg-violet-600/10 blur-3xl" />

        <div className="mx-auto max-w-7xl px-4 sm:px-6 relative z-10">
          <div className="lg:grid lg:grid-cols-12 lg:gap-8 items-center">
            
            {/* Left Content */}
            <div className="sm:text-center md:mx-auto lg:col-span-6 lg:text-left">
              <motion.div {...riseIn(0)} className="inline-flex items-center rounded-full border border-indigo-500/30 bg-indigo-500/10 px-3 py-1 text-xs font-semibold uppercase tracking-wider text-indigo-400">
                <span className="flex h-2 w-2 rounded-full bg-indigo-500 mr-2 animate-pulse"></span>
                New Season Â· New Drops
              </motion.div>
              <motion.h1 {...riseIn(0.1)} className="mt-6 text-4xl font-extrabold tracking-tight text-white sm:text-5xl md:text-6xl lg:text-5xl xl:text-6xl">
                <span className="block xl:inline">Everyday essentials,</span>{' '}
                <span className="block text-indigo-400 xl:inline">elevated.</span>
              </motion.h1>
              <motion.p {...riseIn(0.2)} className="mt-4 text-base text-slate-400 sm:text-lg md:mt-6 max-w-2xl mx-auto lg:mx-0">
                Discover products designed for everyday life, with secure checkout, fast delivery and easy returns. Premium quality guaranteed.
              </motion.p>
              <motion.div {...riseIn(0.3)} className="mt-8 flex flex-col sm:flex-row justify-center lg:justify-start gap-4">
                <Link to="/products" className="inline-flex items-center justify-center rounded-full bg-indigo-600 px-8 py-3.5 text-base font-bold text-white shadow-lg shadow-indigo-900/50 transition hover:bg-indigo-700 hover:scale-[1.02] active:scale-95">
                  Shop Now <FiArrowRight className="ml-2" />
                </Link>
                <Link to="/products?sort=-created_at" className="inline-flex items-center justify-center rounded-full bg-slate-800 px-8 py-3.5 text-base font-bold text-white transition hover:bg-slate-700">
                  Explore New Arrivals
                </Link>
              </motion.div>
            </div>

            {/* Right Product Collage */}
            <div className="mt-16 lg:col-span-6 lg:mt-0 lg:flex lg:justify-end hidden">
              <motion.div 
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.8, delay: 0.2 }}
                className="relative w-full max-w-lg h-[500px]"
              >
                {/* Visual Collage of 3 products */}
                {items.length >= 3 && (
                  <>
                    {/* Top Right */}
                    <div className="absolute right-0 top-0 w-64 h-64 rounded-2xl overflow-hidden border border-slate-700 bg-slate-800 shadow-2xl z-20 translate-x-4 -translate-y-4">
                      <img src={mediaUrl(items[0].image)} className="w-full h-full object-cover opacity-90" alt="" />
                    </div>
                    {/* Bottom Left */}
                    <div className="absolute left-0 bottom-12 w-56 h-56 rounded-2xl overflow-hidden border border-slate-700 bg-slate-800 shadow-2xl z-30 -translate-x-8">
                      <img src={mediaUrl(items[1].image)} className="w-full h-full object-cover opacity-90" alt="" />
                    </div>
                    {/* Center Back */}
                    <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-72 h-72 rounded-2xl overflow-hidden border border-slate-700 bg-slate-800/80 shadow-xl z-10 blur-[1px]">
                      <img src={mediaUrl(items[2].image)} className="w-full h-full object-cover opacity-50" alt="" />
                    </div>
                  </>
                )}
              </motion.div>
            </div>

          </div>
        </div>
      </section>

      {/* ================= Trust Features ================= */}
      <section className="border-b border-slate-800 bg-slate-900/50">
        <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6">
          <div className="grid grid-cols-2 gap-6 lg:grid-cols-4 lg:gap-8">
            {[
              { icon: FiTruck, title: "Fast Shipping", desc: "Free over â‚¹1,500 Â· 2-5 day dispatch" },
              { icon: FiShield, title: "Secure Payments", desc: "Encrypted checkout Â· UPI, cards & more" },
              { icon: FiRefreshCw, title: "Easy Returns", desc: "30-day hassle-free returns" },
              { icon: FiHeadphones, title: "Customer Support", desc: "Friendly support when you need it" },
            ].map((f, i) => (
              <div key={i} className="flex flex-col sm:flex-row items-center sm:items-start text-center sm:text-left gap-4 p-4 rounded-2xl bg-slate-800/20 border border-slate-800/50">
                <div className="flex h-12 w-12 items-center justify-center rounded-full bg-indigo-500/10 text-indigo-400 flex-shrink-0">
                  <f.icon size={24} />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-white">{f.title}</h3>
                  <p className="mt-1 text-xs text-slate-400">{f.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ================= Shop by Category ================= */}
      {availableCategories.length > 0 && (
        <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:py-24">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-extrabold text-white">Shop by Category</h2>
            <p className="mt-3 text-slate-400">Find what fits your everyday.</p>
          </div>
          <div className="grid grid-cols-2 gap-4 md:grid-cols-4 lg:gap-6">
            {availableCategories.slice(0,4).map((cat, i) => {
              const catProduct = items.find(p => p.category_name === cat);
              return (
                <Link key={cat} to={`/products?category=${encodeURIComponent(cat)}`} className="group relative overflow-hidden rounded-2xl bg-slate-800 aspect-[4/5] sm:aspect-square flex flex-col justify-end">
                  {catProduct && (
                    <img src={mediaUrl(catProduct.image)} alt={cat} className="absolute inset-0 h-full w-full object-cover opacity-60 transition-transform duration-700 group-hover:scale-110" />
                  )}
                  <div className="absolute inset-0 bg-gradient-to-t from-slate-900 via-slate-900/40 to-transparent opacity-80" />
                  <div className="relative p-6 z-10">
                    <h3 className="text-lg font-bold text-white group-hover:text-indigo-300 transition-colors">{cat}</h3>
                    <div className="mt-2 flex items-center text-sm font-medium text-indigo-400 opacity-0 transform translate-y-4 transition-all duration-300 group-hover:opacity-100 group-hover:translate-y-0">
                      Explore <FiArrowRight className="ml-1" />
                    </div>
                  </div>
                </Link>
              );
            })}
          </div>
        </section>
      )}

      {/* ================= New Arrivals ================= */}
      <section className="bg-slate-800/30 border-y border-slate-800">
        <div className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:py-24">
          <div className="flex flex-col sm:flex-row justify-between items-end mb-8 gap-4">
            <div>
              <h2 className="text-3xl font-extrabold text-white">New Arrivals</h2>
              <p className="mt-2 text-slate-400">Fresh picks, just added.</p>
            </div>
            <Link to="/products?sort=-created_at" className="flex items-center text-sm font-bold text-indigo-400 hover:text-indigo-300 transition-colors">
              View All <FiArrowRight className="ml-1" />
            </Link>
          </div>

          {/* Category Tabs */}
          {categoryTabs.length > 1 && (
            <div className="flex overflow-x-auto pb-4 mb-6 hide-scrollbar gap-2">
              {categoryTabs.map(tab => (
                <button
                  key={tab}
                  onClick={() => setActiveCategory(tab)}
                  className={`whitespace-nowrap px-5 py-2 rounded-full text-sm font-medium transition-colors ${
                    activeCategory === tab 
                      ? 'bg-indigo-600 text-white' 
                      : 'bg-slate-800 text-slate-400 hover:bg-slate-700 hover:text-white'
                  }`}
                >
                  {tab}
                </button>
              ))}
            </div>
          )}

          <div className="grid grid-cols-2 gap-4 md:grid-cols-3 xl:grid-cols-4 lg:gap-6">
            {loading ? (
              [...Array(4)].map((_, i) => <SkeletonCard key={i} />)
            ) : filteredNewArrivals.length > 0 ? (
              filteredNewArrivals.map((p, i) => (
                <BentoProductCard key={p.id} product={p} index={i} />
              ))
            ) : (
              <div className="col-span-full py-12 text-center text-slate-400">
                No new products available in this category.
              </div>
            )}
          </div>
        </div>
      </section>

      {/* ================= Featured Collection ================= */}
      {featuredProduct && (
        <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:py-24">
          <div className="overflow-hidden rounded-3xl bg-slate-800 border border-slate-700 lg:grid lg:grid-cols-2 lg:items-center">
            <div className="aspect-[4/3] lg:aspect-auto lg:h-[500px] relative">
              <img src={mediaUrl(featuredProduct.image)} alt="Featured" className="absolute inset-0 h-full w-full object-cover opacity-80" />
              <div className="absolute inset-0 bg-gradient-to-r from-transparent to-slate-800 lg:hidden" />
            </div>
            <div className="p-8 sm:p-12 lg:pl-16">
              <h2 className="text-3xl font-extrabold text-white sm:text-4xl">Upgrade your everyday setup</h2>
              <p className="mt-4 text-lg text-slate-400">
                Smart technology and essentials designed for modern life. Experience the perfect blend of form and function.
              </p>
              <div className="mt-8">
                <Link to={`/products?category=${encodeURIComponent(featuredProduct.category_name || '')}`} className="inline-flex items-center justify-center rounded-full bg-white px-8 py-3.5 text-base font-bold text-slate-900 transition hover:bg-slate-200">
                  Shop {featuredProduct.category_name || 'Collection'} <FiArrowRight className="ml-2" />
                </Link>
              </div>
            </div>
          </div>
        </section>
      )}

      {/* ================= Best Sellers ================= */}
      <section className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:py-16">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-extrabold text-white">Best Sellers</h2>
          <p className="mt-3 text-slate-400">Customer favorites worth checking out.</p>
        </div>
        <div className="grid grid-cols-2 gap-4 md:grid-cols-3 xl:grid-cols-4 lg:gap-6">
          {loading ? (
            [...Array(4)].map((_, i) => <SkeletonCard key={i} />)
          ) : bestSellers.length > 0 ? (
            bestSellers.map((p, i) => (
              <BentoProductCard key={p.id} product={p} index={i} />
            ))
          ) : (
            <div className="col-span-full py-12 text-center text-slate-400">
              Popular products will appear here soon.
            </div>
          )}
        </div>
      </section>

      {/* ================= Promotional Banner ================= */}
      <section className="mx-auto max-w-7xl px-4 py-12 sm:px-6">
        <div className="relative rounded-3xl bg-indigo-900 overflow-hidden px-6 py-16 sm:px-12 sm:py-20 lg:px-16 border border-indigo-700/50 shadow-2xl shadow-indigo-900/20">
          <div className="absolute inset-0 bg-[url('data:image/svg+xml,%3Csvg width=\"20\" height=\"20\" viewBox=\"0 0 20 20\" xmlns=\"http://www.w3.org/2000/svg\"%3E%3Cg fill=\"%23818cf8\" fill-opacity=\"0.05\" fill-rule=\"evenodd\"%3E%3Ccircle cx=\"3\" cy=\"3\" r=\"3\"/%3E%3Ccircle cx=\"13\" cy=\"13\" r=\"3\"/%3E%3C/g%3E%3C/svg%3E')] opacity-50"></div>
          <div className="relative mx-auto max-w-2xl text-center">
            <h2 className="text-3xl font-extrabold text-white sm:text-4xl">Up to 30% off selected essentials</h2>
            <p className="mt-4 text-lg text-indigo-200">Limited-time offers on products you love. Don't miss out on our biggest deals of the season.</p>
            <div className="mt-8">
              <Link to="/products?sale=true" className="inline-flex items-center justify-center rounded-full bg-white px-8 py-3.5 text-base font-bold text-indigo-900 shadow-sm transition hover:bg-indigo-50">
                Shop Deals <FiArrowRight className="ml-2" />
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* ================= Newsletter ================= */}
      <section className="border-t border-slate-800 bg-slate-900">
        <div className="mx-auto max-w-4xl px-4 py-16 sm:px-6 lg:py-24 text-center">
          <h2 className="text-3xl font-extrabold text-white">Stay in the loop</h2>
          <p className="mt-4 text-lg text-slate-400">Get new arrivals, exclusive offers and product updates directly to your inbox.</p>
          
          <form onSubmit={handleSubscribe} className="mt-8 sm:flex sm:max-w-md sm:mx-auto relative">
            <label htmlFor="email-address" className="sr-only">Email address</label>
            <input
              type="email"
              id="email-address"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full min-w-0 rounded-full border border-slate-700 bg-slate-800 px-6 py-3.5 text-base text-white placeholder-slate-400 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
              placeholder="Enter your email"
            />
            <div className="mt-3 sm:ml-3 sm:mt-0 sm:flex-shrink-0">
              <button
                type="submit"
                className="flex w-full items-center justify-center rounded-full bg-indigo-600 px-6 py-3.5 text-base font-bold text-white transition hover:bg-indigo-700"
              >
                Subscribe
              </button>
            </div>
          </form>
          
          <AnimatePresence>
            {isSubscribed && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
                className="mt-4 flex items-center justify-center text-sm font-medium text-emerald-400"
              >
                <FiCheck className="mr-2" /> You're subscribed!
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </section>
    </PageTransition>
  );
}
"""

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated HomePage.jsx")
