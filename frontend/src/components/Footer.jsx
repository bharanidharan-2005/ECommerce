import React, { useState } from "react";
import { Link } from "react-router-dom";
import { useDispatch } from "react-redux";
import { applyCoupon } from "../features/cart/cartSlice";
import { FiFacebook, FiTwitter, FiInstagram, FiYoutube, FiArrowRight, FiCheck, FiAlertCircle } from "react-icons/fi";
import api from "../api/axios";

export default function Footer() {
  const dispatch = useDispatch();
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState(""); // 'idle', 'loading', 'success', 'error'
  const [message, setMessage] = useState("");
  const [couponCode, setCouponCode] = useState("");
  const [copied, setCopied] = useState(false);

  const handleSubscribe = async (e) => {
    e.preventDefault();
    if (!email) return;

    setStatus("loading");
    try {
      const response = await api.post("/auth/newsletter/subscribe/", { email });
      setStatus("success");
      setMessage(response.data.message || "Successfully subscribed!");
      const coupon = response.data.coupon || "";
      setCouponCode(coupon);
      setEmail("");
      if (coupon) {
        // We know WELCOME10 gives 10% discount in our backend
        dispatch(applyCoupon({ code: coupon, discount_percentage: 10 }));
      }
    } catch (err) {
      setStatus("error");
      setMessage(err.response?.data?.detail || err.response?.data?.message || err.response?.data?.error || "Failed to subscribe. Please try again.");
    }
  };

  const handleCopyCode = () => {
    if (couponCode) {
      navigator.clipboard.writeText(couponCode);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <footer className="bg-[#050810] pt-24 pb-12 border-t border-slate-800">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 gap-12 lg:grid-cols-12 lg:gap-8 border-b border-slate-800 pb-16">
          
          {/* Brand & Newsletter */}
          <div className="lg:col-span-5">
            <Link to="/" className="flex items-center gap-2 group mb-6 inline-flex">
              <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-indigo-600 text-white transition-transform group-hover:scale-105 group-hover:rotate-3">
                <span className="font-black text-xl leading-none tracking-tighter">S</span>
              </div>
              <span className="text-xl font-bold tracking-tight text-white">
                Shop<span className="text-indigo-400">Verse</span>
              </span>
            </Link>
            <p className="text-slate-400 max-w-md mb-8">
              Everyday essentials, elevated. Discover our curated collection of premium products designed for modern living.
            </p>
            
            <div className="space-y-4">
              {status !== "success" ? (
                <>
                  <h3 className="text-lg font-bold text-white uppercase tracking-wider">GET 10% OFF YOUR FIRST ORDER</h3>
                  <p className="text-slate-400 text-sm mb-4">
                    Subscribe to ShopVerse and get 10% off your first purchase, plus early access to new arrivals and exclusive deals.
                  </p>
                  <form className="flex flex-col sm:flex-row max-w-md gap-2" onSubmit={handleSubscribe}>
                    <input 
                      type="email" 
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="Enter your email address" 
                      disabled={status === "loading"}
                      className="flex-1 rounded-xl bg-slate-900 border border-slate-800 px-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition disabled:opacity-50"
                    />
                    <button 
                      type="submit" 
                      disabled={status === "loading"}
                      className="rounded-xl bg-indigo-600 px-6 py-3 text-sm font-bold text-white hover:bg-indigo-500 transition flex items-center justify-center disabled:opacity-50 whitespace-nowrap"
                    >
                      {status === "loading" ? "Wait..." : "GET 10% OFF"}
                    </button>
                  </form>
                  <p className="text-xs text-slate-500 mt-2">No spam. Unsubscribe anytime.</p>
                  {status === "error" && (
                    <div className="flex items-center gap-2 text-rose-400 text-sm mt-3 bg-rose-500/10 p-3 rounded-lg border border-rose-500/20">
                      <FiAlertCircle className="flex-shrink-0" />
                      <span>{message}</span>
                    </div>
                  )}
                </>
              ) : (
                <div className="bg-slate-900/50 p-6 rounded-2xl border border-indigo-500/30">
                  <div className="flex items-center gap-2 text-emerald-400 font-bold mb-2">
                    <FiCheck size={20} />
                    <span>You're in!</span>
                  </div>
                  <p className="text-white text-sm mb-4">Your 10% discount is ready.</p>
                  
                  {couponCode && (
                    <>
                      <div className="bg-slate-950 border border-slate-800 rounded-xl p-4 flex flex-col items-center justify-center mb-6">
                        <span className="text-xl font-black text-indigo-400 tracking-widest">{couponCode}</span>
                        <span className="text-xs text-slate-400 mt-1 uppercase font-bold tracking-wider">10% OFF your first order</span>
                      </div>
                      <p className="text-xs text-slate-400 text-center mb-6">Minimum order ₹999 • Valid for 7 days</p>
                      
                      <div className="flex flex-col sm:flex-row gap-3">
                        <button 
                          onClick={handleCopyCode}
                          className="flex-1 rounded-xl bg-slate-800 px-4 py-3 text-sm font-bold text-white hover:bg-slate-700 transition flex items-center justify-center border border-slate-700"
                        >
                          {copied ? "✓ Code copied!" : "COPY CODE"}
                        </button>
                        <Link 
                          to="/products"
                          className="flex-1 rounded-xl bg-indigo-600 px-4 py-3 text-sm font-bold text-white hover:bg-indigo-500 transition flex items-center justify-center gap-2"
                        >
                          SHOP NOW <FiArrowRight />
                        </Link>
                      </div>
                    </>
                  )}
                </div>
              )}
            </div>
          </div>

          {/* Links Columns */}
          <div className="lg:col-span-7 grid grid-cols-2 md:grid-cols-3 gap-8">
            {/* Column 1 */}
            <div>
              <h3 className="text-sm font-bold text-white uppercase tracking-wider mb-6">Shop</h3>
              <ul className="space-y-4">
                <li><Link to="/products?category=all" className="text-slate-400 hover:text-indigo-400 transition text-sm">All Categories</Link></li>
                <li><Link to="/products?sort=-created_at" className="text-slate-400 hover:text-indigo-400 transition text-sm">New Arrivals</Link></li>
                <li><Link to="/products?sale=true" className="text-slate-400 hover:text-indigo-400 transition text-sm">Deals & Offers</Link></li>
                <li><Link to="/products" className="text-slate-400 hover:text-indigo-400 transition text-sm">Trending Now</Link></li>
              </ul>
            </div>

            {/* Column 2 */}
            <div>
              <h3 className="text-sm font-bold text-white uppercase tracking-wider mb-6">Support</h3>
              <ul className="space-y-4">
                <li><Link to="/contact" className="text-slate-400 hover:text-indigo-400 transition text-sm">Contact Us</Link></li>
                <li><Link to="/faq" className="text-slate-400 hover:text-indigo-400 transition text-sm">FAQs</Link></li>
                <li><Link to="/shipping" className="text-slate-400 hover:text-indigo-400 transition text-sm">Shipping & Returns</Link></li>
                <li><Link to="/track-order" className="text-slate-400 hover:text-indigo-400 transition text-sm">Track Order</Link></li>
              </ul>
            </div>

            {/* Column 3 */}
            <div className="col-span-2 md:col-span-1">
              <h3 className="text-sm font-bold text-white uppercase tracking-wider mb-6">Company</h3>
              <ul className="space-y-4">
                <li><Link to="/about" className="text-slate-400 hover:text-indigo-400 transition text-sm">About Us</Link></li>
                <li><Link to="/careers" className="text-slate-400 hover:text-indigo-400 transition text-sm">Careers</Link></li>
                <li><Link to="/privacy" className="text-slate-400 hover:text-indigo-400 transition text-sm">Privacy Policy</Link></li>
                <li><Link to="/terms" className="text-slate-400 hover:text-indigo-400 transition text-sm">Terms of Service</Link></li>
              </ul>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="pt-8 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-sm text-slate-500">
            &copy; {new Date().getFullYear()} ShopVerse. All rights reserved.
          </p>
          <div className="flex items-center gap-6">
            <a href="#" className="text-slate-500 hover:text-white transition"><FiFacebook size={20} /></a>
            <a href="#" className="text-slate-500 hover:text-white transition"><FiTwitter size={20} /></a>
            <a href="#" className="text-slate-500 hover:text-white transition"><FiInstagram size={20} /></a>
            <a href="#" className="text-slate-500 hover:text-white transition"><FiYoutube size={20} /></a>
          </div>
        </div>
      </div>
    </footer>
  );
}