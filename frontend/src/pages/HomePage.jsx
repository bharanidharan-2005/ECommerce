import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { FiArrowRight, FiShield, FiTruck, FiRefreshCw, FiStar } from "react-icons/fi";
import { motion } from "framer-motion";
import { fetchProducts, selectProducts } from "../features/products/productsSlice";
import BentoProductCard from "../components/BentoProductCard";

const categories = [
  {
    name: "Electronics",
    image: "https://images.unsplash.com/photo-1498049794561-7780e7231661?q=80&w=2070&auto=format&fit=crop",
    link: "/products?category=electronics",
    count: "120+ Items"
  },
  {
    name: "Fashion",
    image: "https://images.unsplash.com/photo-1445205170230-053b83016050?q=80&w=2071&auto=format&fit=crop",
    link: "/products?category=fashion",
    count: "90+ Items"
  },
  {
    name: "Accessories",
    image: "https://images.unsplash.com/photo-1584916201218-f4242ceb4809?q=80&w=2070&auto=format&fit=crop",
    link: "/products?category=accessories",
    count: "45+ Items"
  },
  {
    name: "Home & Living",
    image: "https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?q=80&w=2069&auto=format&fit=crop",
    link: "/products?category=home",
    count: "60+ Items"
  }
];

const features = [
  { icon: FiTruck, title: "Free Global Shipping", desc: "On qualifying orders" },
  { icon: FiShield, title: "Secure Payments", desc: "256-bit SSL encryption" },
  { icon: FiRefreshCw, title: "Easy Returns", desc: "30-day return policy" },
  { icon: FiStar, title: "Premium Quality", desc: "Top-grade materials" }
];

export default function HomePage() {
  const dispatch = useDispatch();
  const { items: products, loading } = useSelector(selectProducts);
  const [promotion, setPromotion] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8010/api/products/promotions/active/')
      .then(res => {
        if (!res.ok) throw new Error('No active promotion');
        return res.json();
      })
      .then(data => setPromotion(data))
      .catch(err => {
        console.log(err.message);
        setPromotion(null);
      });
  }, []);


  useEffect(() => {
    dispatch(fetchProducts({ page: 1, limit: 8 }));
  }, [dispatch]);

  const trendingProducts = products?.slice(0, 4) || [];
  const newArrivals = products?.slice(4, 8) || [];

  return (
    <div className="min-h-screen bg-[#0B1020]">
      {/* Hero Section */}
      <section className="relative flex min-h-[550px] items-center justify-center overflow-hidden pt-20">
        {/* Background Elements */}
        <div className="absolute inset-0 bg-gradient-to-b from-indigo-900/20 to-[#0B1020]"></div>
        <div className="absolute top-1/4 right-1/4 h-96 w-96 rounded-full bg-indigo-500/10 blur-[120px]"></div>
        <div className="absolute bottom-1/4 left-1/4 h-96 w-96 rounded-full bg-purple-500/10 blur-[120px]"></div>
        
        <div className="relative z-10 mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <span className="mb-4 inline-block rounded-full bg-indigo-500/10 px-4 py-1.5 text-xs font-bold tracking-wider text-indigo-400 border border-indigo-500/20">
              NEW SEASON • NEW DROPS
            </span>
            <h1 className="mb-6 text-5xl font-black tracking-tight text-white sm:text-7xl lg:text-8xl">
              Everyday essentials,<br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-purple-400">elevated.</span>
            </h1>
            <p className="mx-auto mb-10 max-w-2xl text-lg text-slate-400 sm:text-xl">
              Discover our curated collection of premium products designed for modern living. 
              Uncompromising quality meets exceptional design.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/products"
                className="inline-flex items-center justify-center gap-2 rounded-full bg-indigo-600 px-8 py-4 text-sm font-bold text-white transition-all hover:bg-indigo-500 hover:shadow-lg hover:shadow-indigo-500/25"
              >
                Shop Collection <FiArrowRight />
              </Link>
              <Link
                to="/products?category=all"
                className="inline-flex items-center justify-center gap-2 rounded-full bg-slate-800 px-8 py-4 text-sm font-bold text-white transition-all hover:bg-slate-700 border border-slate-700"
              >
                Explore Categories
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Trust Features */}
      <section className="bg-slate-900/50 backdrop-blur">
        <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 gap-8 md:grid-cols-4">
            {features.map((feature, idx) => (
              <div key={idx} className="flex flex-col items-center text-center">
                <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-2xl bg-indigo-500/10 text-indigo-400">
                  <feature.icon size={24} />
                </div>
                <h3 className="mb-1 text-sm font-bold text-white">{feature.title}</h3>
                <p className="text-xs text-slate-400">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Shop by Category */}
      <section className="mx-auto max-w-7xl px-4 py-24 sm:px-6 lg:px-8">
        <div className="mb-12 flex items-end justify-between">
          <div>
            <h2 className="text-3xl font-black text-white sm:text-4xl">Shop by Category</h2>
            <p className="mt-2 text-slate-400">Find exactly what you're looking for</p>
          </div>
          <Link to="/products?category=all" className="hidden text-sm font-bold text-indigo-400 transition hover:text-indigo-300 sm:flex items-center gap-1">
            View All <FiArrowRight />
          </Link>
        </div>
        
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {categories.map((cat, idx) => (
            <Link key={idx} to={cat.link} className="group relative overflow-hidden rounded-3xl bg-slate-800 aspect-[4/5]">
              <div className="absolute inset-0 bg-gradient-to-t from-slate-900 via-slate-900/20 to-transparent z-10 transition-opacity duration-300 group-hover:opacity-90"></div>
              <img
                src={cat.image}
                alt={cat.name}
                className="absolute inset-0 h-full w-full object-cover transition-transform duration-700 group-hover:scale-110"
              />
              <div className="absolute inset-0 z-20 flex flex-col justify-end p-6">
                <span className="mb-1 text-xs font-bold uppercase tracking-wider text-indigo-400 opacity-0 transform translate-y-4 transition-all duration-300 group-hover:opacity-100 group-hover:translate-y-0">
                  {cat.count}
                </span>
                <h3 className="text-2xl font-bold text-white">{cat.name}</h3>
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* Trending Products */}
      <section className="bg-slate-900/30 py-24">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="mb-12 flex items-end justify-between">
            <div>
              <h2 className="text-3xl font-black text-white sm:text-4xl">Trending Now</h2>
              <p className="mt-2 text-slate-400">Our most popular pieces this week</p>
            </div>
            <Link to="/products" className="hidden text-sm font-bold text-indigo-400 transition hover:text-indigo-300 sm:flex items-center gap-1">
              View Collection <FiArrowRight />
            </Link>
          </div>

          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {loading ? (
              [...Array(4)].map((_, i) => (
                <div key={i} className="h-96 rounded-3xl bg-slate-800 animate-pulse"></div>
              ))
            ) : trendingProducts.length > 0 ? (
              trendingProducts.map(product => (
                <BentoProductCard key={product.id} product={product} />
              ))
            ) : (
              <p className="text-slate-400 col-span-full">No trending products found.</p>
            )}
          </div>
        </div>
      </section>

      {/* Promo Banner */}
      <section className="mx-auto max-w-7xl px-4 py-24 sm:px-6 lg:px-8">
        <div className="relative overflow-hidden rounded-[2.5rem] bg-indigo-600">
          <div className="absolute inset-0 bg-[url('https://images.unsplash.com/photo-1618220179428-22790b46a0eb?q=80&w=2070&auto=format&fit=crop')] bg-cover bg-center mix-blend-overlay opacity-20"></div>
          <div className="relative z-10 p-12 sm:p-20 flex flex-col items-center text-center lg:items-start lg:text-left">
            <span className="mb-4 inline-block rounded-full bg-white/20 px-4 py-1.5 text-xs font-bold tracking-wider text-white backdrop-blur-md">
              {promotion ? promotion.badge : "FEATURED"}
            </span>
            <h2 className="mb-4 text-4xl font-black text-white sm:text-5xl lg:text-6xl">
              {promotion ? promotion.title : "ShopVerse Picks"}
            </h2>
            <p className="mb-8 max-w-xl text-lg text-indigo-100">
              {promotion ? promotion.description : "Discover our curated selection of top-rated tech and gaming gear."}
            </p>
            <Link
              to={promotion && promotion.category_slug ? "/products?category=" + promotion.category_slug : "/products"}
              className="inline-flex items-center justify-center rounded-full bg-white px-8 py-4 text-sm font-bold text-indigo-600 transition hover:bg-indigo-50"
            >
              {promotion ? promotion.button_text : "Explore Collection"}
            </Link>
          </div>
        </div>
      </section>

      {/* New Arrivals */}
      <section className="mx-auto max-w-7xl px-4 pb-24 sm:px-6 lg:px-8">
        <div className="mb-12 flex items-end justify-between">
          <div>
            <h2 className="text-3xl font-black text-white sm:text-4xl">New Arrivals</h2>
            <p className="mt-2 text-slate-400">Fresh styles just landed</p>
          </div>
          <Link to="/products?sort=-created_at" className="hidden text-sm font-bold text-indigo-400 transition hover:text-indigo-300 sm:flex items-center gap-1">
            View All <FiArrowRight />
          </Link>
        </div>

        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {loading ? (
            [...Array(4)].map((_, i) => (
              <div key={i} className="h-96 rounded-3xl bg-slate-800 animate-pulse"></div>
            ))
          ) : newArrivals.length > 0 ? (
            newArrivals.map(product => (
              <BentoProductCard key={product.id} product={product} />
            ))
          ) : (
            <p className="text-slate-400 col-span-full">No new arrivals found.</p>
          )}
        </div>
      </section>
    </div>
  );
}