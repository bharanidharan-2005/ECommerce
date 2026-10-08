import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { FiX, FiCheck, FiArrowRight, FiAlertCircle } from "react-icons/fi";
import api from "../api/axios";

export default function WelcomePopup() {
  const [isOpen, setIsOpen] = useState(false);
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState(""); // 'idle', 'loading', 'success', 'error'
  const [message, setMessage] = useState("");
  const [couponCode, setCouponCode] = useState("");
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    // Check if the user has already seen the popup or is subscribed
    const hasSeenPopup = localStorage.getItem("shopverse_welcome_seen");
    const isSubscribed = localStorage.getItem("shopverse_subscribed");
    
    if (!hasSeenPopup && !isSubscribed) {
      // Show popup after 5 seconds
      const timer = setTimeout(() => {
        setIsOpen(true);
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, []);

  const handleClose = () => {
    setIsOpen(false);
    localStorage.setItem("shopverse_welcome_seen", "true");
  };

  const handleSubscribe = async (e) => {
    e.preventDefault();
    if (!email) return;

    setStatus("loading");
    try {
      const response = await api.post("/auth/newsletter/subscribe/", { email });
      setStatus("success");
      setMessage(response.data.message || "Successfully subscribed!");
      setCouponCode(response.data.coupon || "");
      localStorage.setItem("shopverse_subscribed", "true");
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

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6">
      {/* Backdrop */}
      <div 
        className="fixed inset-0 bg-black/60 backdrop-blur-sm transition-opacity" 
        onClick={handleClose}
      />
      
      {/* Modal */}
      <div className="relative w-full max-w-md transform overflow-hidden rounded-2xl bg-[#0B1020] border border-slate-800 shadow-2xl transition-all flex flex-col">
        {/* Close button */}
        <button 
          onClick={handleClose}
          className="absolute right-4 top-4 text-slate-400 hover:text-white bg-slate-900/50 hover:bg-slate-800 p-2 rounded-full transition-colors z-10"
          aria-label="Close"
        >
          <FiX size={20} />
        </button>

        <div className="p-8 sm:p-10">
          <div className="flex items-center gap-2 group mb-8 justify-center inline-flex w-full">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-indigo-600 text-white">
              <span className="font-black text-xl leading-none tracking-tighter">S</span>
            </div>
            <span className="text-xl font-bold tracking-tight text-white uppercase">
              Welcome to Shop<span className="text-indigo-400">Verse</span>
            </span>
          </div>

          {status !== "success" ? (
            <>
              <h2 className="text-2xl font-black text-white text-center mb-3">
                GET 10% OFF<br/>YOUR FIRST ORDER
              </h2>
              <p className="text-slate-400 text-center text-sm mb-8 leading-relaxed">
                Subscribe and receive your first-order discount plus early access to new arrivals and exclusive deals.
              </p>

              <form onSubmit={handleSubscribe} className="space-y-4">
                <div>
                  <input 
                    type="email" 
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Enter your email address" 
                    disabled={status === "loading"}
                    className="w-full rounded-xl bg-slate-900 border border-slate-700 px-4 py-3.5 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition disabled:opacity-50 text-center"
                  />
                </div>
                <button 
                  type="submit" 
                  disabled={status === "loading"}
                  className="w-full rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 px-6 py-3.5 text-sm font-bold text-white hover:from-indigo-500 hover:to-purple-500 transition flex items-center justify-center disabled:opacity-50 shadow-lg shadow-indigo-500/20"
                >
                  {status === "loading" ? "Wait..." : "GET MY 10% OFF"}
                </button>
              </form>
              
              {status === "error" && (
                <div className="flex items-center justify-center gap-2 text-rose-400 text-sm mt-4 bg-rose-500/10 p-3 rounded-lg border border-rose-500/20">
                  <FiAlertCircle className="flex-shrink-0" />
                  <span>{message}</span>
                </div>
              )}

              <div className="mt-6 flex flex-col items-center gap-3">
                <p className="text-xs text-slate-500">No spam. Unsubscribe anytime.</p>
                <button 
                  onClick={handleClose}
                  className="text-xs font-semibold text-slate-400 hover:text-white transition underline underline-offset-4"
                >
                  No thanks
                </button>
              </div>
            </>
          ) : (
            <div className="flex flex-col items-center text-center">
              <div className="h-16 w-16 bg-emerald-500/20 rounded-full flex items-center justify-center mb-6">
                <FiCheck className="text-emerald-400" size={32} />
              </div>
              
              <h2 className="text-2xl font-black text-white mb-2">You're in!</h2>
              <p className="text-slate-300 mb-8">Your 10% discount is ready.</p>
              
              {couponCode && (
                <div className="w-full">
                  <div className="bg-slate-900 border-2 border-indigo-500/30 border-dashed rounded-xl p-5 flex flex-col items-center justify-center mb-6">
                    <span className="text-2xl font-black text-indigo-400 tracking-widest">{couponCode}</span>
                    <span className="text-xs text-slate-400 mt-2 uppercase font-bold tracking-wider">10% OFF your first order</span>
                  </div>
                  <p className="text-xs text-slate-400 text-center mb-6">Minimum order ₹999 • Valid for 7 days</p>
                  
                  <div className="flex flex-col gap-3">
                    <button 
                      onClick={handleCopyCode}
                      className="w-full rounded-xl bg-slate-800 px-4 py-3.5 text-sm font-bold text-white hover:bg-slate-700 transition flex items-center justify-center border border-slate-700"
                    >
                      {copied ? "✓ Code copied!" : "COPY CODE"}
                    </button>
                    <Link 
                      to="/products"
                      onClick={handleClose}
                      className="w-full rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 px-4 py-3.5 text-sm font-bold text-white hover:from-indigo-500 hover:to-purple-500 transition flex items-center justify-center gap-2 shadow-lg shadow-indigo-500/20"
                    >
                      SHOP NOW <FiArrowRight />
                    </Link>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}