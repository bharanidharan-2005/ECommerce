import React, { useState, useEffect } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import { motion, AnimatePresence } from "framer-motion";
import { 
  FiCheck, FiClock, FiPackage, FiRefreshCw, FiFlag, FiDollarSign, 
  FiXCircle, FiUser, FiMapPin, FiShield, FiBell, FiCreditCard, FiArrowLeft
} from "react-icons/fi";
import api from "../api/axios";
import { toast } from "react-hot-toast";

import { selectCountry, selectCurrency } from "../features/ui/uiSlice";
import { formatPrice, selectProducts } from "../features/products/productsSlice";
import { updateUser } from "../features/auth/authSlice";
import { saveShippingAddress } from "../features/cart/cartSlice";


import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix for default marker icon in leaflet + webpack/vite
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

import PageTransition from "../components/PageTransition.jsx";
import EmptyState from "../components/ui/EmptyState.jsx";
import useFetchOrders from "../utils/useFetchOrders.js";

/** Canonical tracking stages and which backend statuses map to them */
const orderStagesDefault = [
  { id: "pending", label: "Order Placed" },
  { id: "paid", label: "Paid" },
  { id: "shipped", label: "Shipped" },
  { id: "delivered", label: "Delivered" }
];

const orderStagesCOD = [
  { id: "pending", label: "Order Placed" },
  { id: "shipped", label: "Shipped" },
  { id: "paid", label: "Paid" },
  { id: "delivered", label: "Delivered" }
];

const LiveTracker = () => {
  const [loc, setLoc] = useState(null);
  const [err, setErr] = useState('');

  useEffect(() => {
    const fallbackToIP = async () => {
      try {
        const res = await fetch('https://get.geojs.io/v1/ip/geo.json');
        const data = await res.json();
        if (data.latitude && data.longitude) {
          setLoc({ lat: parseFloat(data.latitude), lon: parseFloat(data.longitude) });
        } else {
          setLoc({ lat: 40.7128, lon: -74.0060 });
        }
      } catch (e) {
        setLoc({ lat: 40.7128, lon: -74.0060 });
      }
    };

    let watchId;
    if (navigator.geolocation) {
      watchId = navigator.geolocation.watchPosition(
        (pos) => setLoc({ lat: pos.coords.latitude, lon: pos.coords.longitude }),
        (error) => fallbackToIP(),
        { enableHighAccuracy: true, timeout: 5000, maximumAge: 0 }
      );
    } else {
      fallbackToIP();
    }

    return () => {
      if (watchId !== undefined && navigator.geolocation) {
        navigator.geolocation.clearWatch(watchId);
      }
    };
  }, []);

  if (err) return <div className="mt-4 p-4 text-sm text-red-400 bg-red-500/10 rounded-xl border border-red-500/20">{err}</div>;
  if (!loc) return <div className="mt-4 p-4 text-sm animate-pulse bg-slate-800 rounded-xl">Locating delivery vehicle...</div>;

  return (
    <div className="mt-6 rounded-xl overflow-hidden border border-slate-700 bg-slate-800">
      <div className="bg-slate-800/80 p-3 text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-2 border-b border-slate-700">
        <FiMapPin /> Real-time Delivery Location
      </div>
      <div style={{ height: "300px", width: "100%" }}>
        <MapContainer 
          center={[loc.lat, loc.lon]} 
          zoom={14} 
          scrollWheelZoom={false} 
          style={{ height: "100%", width: "100%", zIndex: 0 }}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
          />
          <Marker position={[loc.lat, loc.lon]}>
            <Popup className="text-slate-900 font-medium">
              Delivery in progress! <br /> We are here.
            </Popup>
          </Marker>
        </MapContainer>
      </div>
    </div>
  );
};


// --- ADDRESS MANAGER COMPONENT ---
const AddressManager = () => {
  const dispatch = useDispatch();
  const savedAddress = useSelector((s) => s.cart.shippingAddress);
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    full_name: "",
    address_line_1: "",
    address_line_2: "",
    city: "",
    state: "",
    postal_code: "",
    country: "US"
  });

  useEffect(() => {
    if (savedAddress) {
      setFormData(savedAddress);
    }
  }, [savedAddress]);

  const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSave = (e) => {
    e.preventDefault();
    dispatch(saveShippingAddress(formData));
    setIsEditing(false);
    toast.success("Address saved successfully!");
  };

  const inputClass = "w-full rounded-xl border border-slate-700 bg-slate-800/50 px-4 py-3 text-sm text-white placeholder-slate-500 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 transition-colors";

  if (isEditing) {
    return (
      <form onSubmit={handleSave} className="space-y-4">
        <input name="full_name" required value={formData.full_name} onChange={handleChange} placeholder="Full Name" className={inputClass} />
        <input name="address_line_1" required value={formData.address_line_1} onChange={handleChange} placeholder="Street Address" className={inputClass} />
        <input name="address_line_2" value={formData.address_line_2} onChange={handleChange} placeholder="Apt, Suite, Unit (optional)" className={inputClass} />
        <div className="grid grid-cols-2 gap-4">
          <input name="city" required value={formData.city} onChange={handleChange} placeholder="City" className={inputClass} />
          <input name="state" required value={formData.state} onChange={handleChange} placeholder="State / Province" className={inputClass} />
        </div>
        <div className="grid grid-cols-2 gap-4">
          <input name="postal_code" required value={formData.postal_code} onChange={handleChange} placeholder="Postal Code" className={inputClass} />
          <input name="country" required value={formData.country} onChange={handleChange} placeholder="Country" className={inputClass} />
        </div>
        <div className="flex gap-3 pt-2">
          <button type="button" onClick={() => setIsEditing(false)} className="btn-outline w-full !py-2">Cancel</button>
          <button type="submit" className="btn-primary w-full !py-2">Save Address</button>
        </div>
      </form>
    );
  }

  return (
    <>
      {!savedAddress ? (
        <div className="flex flex-col items-center justify-center py-6 text-center text-slate-400 border border-dashed border-slate-700 rounded-xl">
          <p className="text-sm">No saved addresses yet.</p>
          <button onClick={() => setIsEditing(true)} className="mt-3 text-indigo-400 text-sm font-bold hover:text-indigo-300 transition-colors">+ Add Address</button>
        </div>
      ) : (
        <div className="bg-slate-800/50 rounded-xl p-4 border border-slate-700 text-sm">
          <p className="font-bold text-white mb-1">{savedAddress.full_name}</p>
          <p className="text-slate-400">{savedAddress.address_line_1}</p>
          {savedAddress.address_line_2 && <p className="text-slate-400">{savedAddress.address_line_2}</p>}
          <p className="text-slate-400">{savedAddress.city}, {savedAddress.state} {savedAddress.postal_code}</p>
          <p className="text-slate-400">{savedAddress.country}</p>
          <button onClick={() => setIsEditing(true)} className="mt-4 text-indigo-400 font-bold hover:text-indigo-300 transition-colors">Edit Address</button>
        </div>
      )}
    </>
  );
};


// --- COUPON MANAGER COMPONENT ---
const CouponManager = () => {
  const [coupon, setCoupon] = useState("");
  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchCoupon = async () => {
      try {
        const { data } = await api.get("/auth/profile/coupon/");
        if (data.coupon) {
          setCoupon(data.coupon);
        } else {
          setError("You don't have a custom promo code yet.");
        }
      } catch (err) {
        setError("You are not subscribed to the newsletter.");
      } finally {
        setLoading(false);
      }
    };
    fetchCoupon();
  }, []);

  const handleSave = async (e) => {
    e.preventDefault();
    try {
      const { data } = await api.put("/auth/profile/coupon/", { coupon });
      setCoupon(data.coupon);
      setIsEditing(false);
      toast.success(data.message || "Promo code updated!");
    } catch (err) {
      toast.error(err.response?.data?.error || "Failed to update promo code");
    }
  };

  const inputClass = "w-full rounded-xl border border-slate-700 bg-slate-800/50 px-4 py-3 text-sm text-white placeholder-slate-500 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 transition-colors uppercase";

  if (loading) return <div className="animate-pulse bg-slate-800 h-24 rounded-xl"></div>;

  return (
    <div className="card p-6 h-full flex flex-col">
      <h2 className="text-lg font-black tracking-tight mb-4 flex items-center gap-2">
        <FiDollarSign className="text-indigo-500" /> My Promo Code
      </h2>
      
      {error ? (
        <div className="flex flex-col items-center justify-center flex-1 text-center text-slate-400 border border-dashed border-slate-700 rounded-xl p-4">
          <p className="text-sm">{error}</p>
        </div>
      ) : isEditing ? (
        <form onSubmit={handleSave} className="space-y-4">
          <input 
            value={coupon} 
            onChange={(e) => setCoupon(e.target.value.toUpperCase())} 
            placeholder="Enter Custom Code" 
            className={inputClass}
            maxLength={15}
            required 
          />
          <div className="flex gap-3">
            <button type="button" onClick={() => setIsEditing(false)} className="btn-outline w-full !py-2">Cancel</button>
            <button type="submit" className="btn-primary w-full !py-2">Save</button>
          </div>
        </form>
      ) : (
        <div className="bg-emerald-500/10 border border-emerald-500/20 rounded-xl p-4 text-center flex flex-col justify-center flex-1">
          <p className="text-xs text-emerald-400/80 font-bold uppercase tracking-wider mb-2">Share this code for 10% off</p>
          <div className="text-2xl font-black text-emerald-400 tracking-widest">{coupon}</div>
          <button onClick={() => setIsEditing(true)} className="mt-4 text-emerald-400 text-sm font-bold hover:text-emerald-300 transition-colors underline underline-offset-4 decoration-emerald-500/30">Change Code</button>
        </div>
      )}
    </div>
  );
};

// --- ACCOUNT TAB COMPONENT ---


const AccountTab = ({ user }) => {
  const dispatch = useDispatch();
  const [formData, setFormData] = useState({
    username: user?.username || "",
    first_name: user?.first_name || "",
    last_name: user?.last_name || "",
    phone: user?.phone || "",
  });
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSave = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const { data } = await api.put("/accounts/profile/", formData);
      dispatch(updateUser(data));
      toast.success("Profile updated successfully!");
    } catch (err) {
      toast.error(err.response?.data?.detail || "Failed to update profile.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      <div className="card p-6 sm:p-8">
        <h2 className="text-lg font-black tracking-tight mb-6 flex items-center gap-2">
          <FiUser className="text-indigo-500" /> Personal Information
        </h2>
        <form onSubmit={handleSave} className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div className="sm:col-span-2">
            <label className="mb-2 block text-xs font-bold uppercase tracking-wider text-slate-400">Username</label>
            <input name="username" value={formData.username} onChange={handleChange} className="w-full rounded-xl border border-slate-700 bg-slate-800/50 px-4 py-3 text-sm text-white placeholder-slate-500 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 transition-colors" />
          </div>
          <div>
            <label className="mb-2 block text-xs font-bold uppercase tracking-wider text-slate-400">First Name</label>
            <input name="first_name" value={formData.first_name} onChange={handleChange} className="w-full rounded-xl border border-slate-700 bg-slate-800/50 px-4 py-3 text-sm text-white placeholder-slate-500 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 transition-colors" placeholder="First Name" />
          </div>
          <div>
            <label className="mb-2 block text-xs font-bold uppercase tracking-wider text-slate-400">Last Name</label>
            <input name="last_name" value={formData.last_name} onChange={handleChange} className="w-full rounded-xl border border-slate-700 bg-slate-800/50 px-4 py-3 text-sm text-white placeholder-slate-500 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 transition-colors" placeholder="Last Name" />
          </div>
          <div>
            <label className="mb-2 block text-xs font-bold uppercase tracking-wider text-slate-400">Email (Read Only)</label>
            <input value={user?.email || ""} disabled className="w-full rounded-xl border border-slate-700 bg-slate-800/30 px-4 py-3 text-sm text-slate-500 cursor-not-allowed" />
          </div>
          <div>
            <label className="mb-2 block text-xs font-bold uppercase tracking-wider text-slate-400">Phone</label>
            <input name="phone" value={formData.phone} onChange={handleChange} className="w-full rounded-xl border border-slate-700 bg-slate-800/50 px-4 py-3 text-sm text-white placeholder-slate-500 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 transition-colors" placeholder="Phone Number" />
          </div>
          <div className="sm:col-span-2 mt-2">
            <button type="submit" disabled={loading} className="btn-primary w-full sm:w-auto">
              {loading ? "Saving..." : "Save Changes"}
            </button>
          </div>
        </form>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="card p-6">
          <h2 className="text-lg font-black tracking-tight mb-4 flex items-center gap-2">
            <FiMapPin className="text-indigo-500" /> Saved Addresses
          </h2>
          <AddressManager />
        </div>
        
        <div className="card p-6">
          <h2 className="text-lg font-black tracking-tight mb-4 flex items-center gap-2">
            <FiBell className="text-indigo-500" /> Notifications
          </h2>
          <div className="space-y-4">
            {['Order Updates', 'Promotional Emails', 'Deals & Offers'].map(n => (
              <div key={n} className="flex items-center justify-between">
                <span className="text-sm font-medium text-slate-300">{n}</span>
                <div className="w-10 h-5 bg-indigo-500 rounded-full relative cursor-pointer">
                  <div className="w-4 h-4 bg-white rounded-full absolute right-0.5 top-0.5 shadow-sm"></div>
                </div>
              </div>
            ))}
          </div>
        </div>
        <CouponManager />
      </div>
    </div>
  );
};

// --- ORDER DETAILS SUB-COMPONENT ---
const OrderDetails = ({ order, onBack, onCancel, userCurrency, rates }) => {
  const isCOD = order?.payment_method === "cod";
  const stages = isCOD ? orderStagesCOD : orderStagesDefault;
  
  let current = stages.findIndex(s => s.id === order?.status);
  if (current === -1) current = 0;
  if (!isCOD && order.is_paid && current < 1) current = 1;

  const cancelled = order?.status === "cancelled";

  return (
    <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }}>
      <button onClick={onBack} className="mb-6 flex items-center gap-2 text-sm font-bold text-slate-400 hover:text-indigo-400 transition-colors">
        <FiArrowLeft /> Back to Orders
      </button>

      <div className="card p-6 sm:p-8">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-800 pb-6 mb-6">
          <div>
            <h2 className="text-xl font-black tracking-tight text-white">Order #{order.order_number}</h2>
            <p className="text-sm text-slate-400 mt-1 flex items-center gap-2">
              <FiClock /> {new Date(order.created_at).toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
            </p>
          </div>
          <div className="flex items-center gap-4">
            <span className={`px-4 py-1.5 rounded-full text-xs font-bold uppercase tracking-wider ${cancelled ? 'bg-red-500/10 text-red-400' : 'bg-indigo-500/10 text-indigo-400'}`}>
              {cancelled ? 'Cancelled' : order.status}
            </span>
            {order.status === "pending" && !cancelled && (
              <button onClick={() => onCancel(order.id)} className="btn-outline !py-1.5 !px-4 !text-xs !text-red-400 !border-red-500/30 hover:!bg-red-500/10">
                Cancel Order
              </button>
            )}
          </div>
        </div>

        {/* Tracking Timeline */}
        {!cancelled && (
          <div className="mb-10">
            <h3 className="text-sm font-bold uppercase tracking-wider text-slate-500 mb-6">Order Tracking</h3>
            <ol className="flex items-start px-1">
              {stages.map((stageObj, i) => {
                const done = i <= current;
                const isLast = i === stages.length - 1;
                return (
                  <li key={stageObj.id} className="flex flex-col items-center flex-1">
                    <div className="relative flex w-full items-center justify-center">
                      {!isLast && <span className={`absolute left-1/2 h-1 w-full ${i < current ? "bg-indigo-500" : "bg-slate-800"}`} />}
                      <span className={`relative z-10 flex h-8 w-8 items-center justify-center rounded-full text-xs font-bold transition-colors ${done ? "bg-indigo-500 text-white" : "border-2 border-slate-700 bg-slate-800 text-slate-500"}`}>
                        {done ? <FiCheck size={14} /> : i + 1}
                      </span>
                    </div>
                    <span className={`mt-3 text-center text-[10px] sm:text-xs font-bold uppercase tracking-wider ${done ? "text-indigo-400" : "text-slate-500"}`}>
                      {stageObj.label}
                    </span>
                  </li>
                );
              })}
            </ol>
            {/* Live Map if Shipped */}
            {order.status === "shipped" && <LiveTracker />}
          </div>
        )}

        {/* Order details grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2 space-y-4">
            <h3 className="text-sm font-bold uppercase tracking-wider text-slate-500">Ordered Products</h3>
            {(order.items || []).map(it => (
              <div key={it.id} className="flex items-center gap-4 bg-slate-800/30 border border-slate-800 rounded-xl p-3">
                {it.image ? (
                  <img src={it.image} alt={it.product_name} className="w-16 h-16 rounded-lg object-cover ring-1 ring-slate-700" />
                ) : (
                  <div className="w-16 h-16 rounded-lg bg-slate-800 flex items-center justify-center text-slate-500">
                    <FiPackage size={24} />
                  </div>
                )}
                <div className="flex-1">
                  <Link to={`/product/${it.product_id || it.product}`} className="font-bold text-slate-200 hover:text-indigo-400 transition-colors line-clamp-1">{it.product_name}</Link>
                  <p className="text-xs text-slate-400 mt-1">Qty: <span className="text-slate-200 font-semibold">{it.quantity}</span></p>
                </div>
                <div className="font-black text-slate-200">
                  {formatPrice(Number(it.price) * it.quantity, userCurrency, rates)}
                </div>
              </div>
            ))}
          </div>

          <div className="space-y-6">
            <div className="bg-slate-800/30 border border-slate-800 rounded-xl p-5">
              <h3 className="text-sm font-bold uppercase tracking-wider text-slate-500 mb-4">Order Summary</h3>
              <div className="space-y-3 text-sm">
                <div className="flex justify-between text-slate-300">
                  <span>Subtotal</span>
                  <span>{formatPrice(Number(order.total_price), userCurrency, rates)}</span>
                </div>
                <div className="flex justify-between text-slate-300">
                  <span>Shipping</span>
                  <span>Free</span>
                </div>
                <div className="border-t border-slate-700 pt-3 flex justify-between font-black text-lg text-white">
                  <span>Total</span>
                  <span>{formatPrice(Number(order.total_price), userCurrency, rates)}</span>
                </div>
              </div>
            </div>

            <div className="bg-slate-800/30 border border-slate-800 rounded-xl p-5 text-sm">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-3">Shipping Address</h3>
              <p className="font-semibold text-slate-200">{order.full_name}</p>
              <p className="text-slate-400 mt-1">{order.address_line_1}</p>
              {order.address_line_2 && <p className="text-slate-400">{order.address_line_2}</p>}
              <p className="text-slate-400">{order.city}, {order.state} {order.postal_code}</p>
              <p className="text-slate-400">{order.country}</p>
            </div>
            
            <div className="bg-slate-800/30 border border-slate-800 rounded-xl p-5 text-sm">
              <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-3">Payment Info</h3>
              <p className="text-slate-300 flex items-center gap-2">
                <span className={`w-2 h-2 rounded-full ${order.is_paid ? 'bg-emerald-500' : 'bg-amber-500'}`}></span>
                {order.is_paid ? 'Paid' : 'Pending'} via {(order.payment_method || "unknown").toUpperCase().replace('_', ' ')}
              </p>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

// --- ORDERS TAB COMPONENT ---
const OrdersTab = ({ orders, loading, refresh, userCurrency, rates, handleCancelOrder }) => {
  const [filter, setFilter] = useState("all");
  const [selectedOrder, setSelectedOrder] = useState(null);

  if (selectedOrder) {
    return <OrderDetails order={selectedOrder} onBack={() => setSelectedOrder(null)} onCancel={handleCancelOrder} userCurrency={userCurrency} rates={rates} />;
  }

  const filteredOrders = orders.filter(o => {
    if (filter === "all") return true;
    return o.status === filter;
  });

  const filters = [
    { id: "all", label: "All" },
    { id: "pending", label: "Pending" },
    { id: "paid", label: "Paid" },
    { id: "shipped", label: "Shipped" },
    { id: "delivered", label: "Delivered" },
    { id: "cancelled", label: "Cancelled" },
  ];

  return (
    <div className="space-y-6">
      {/* Header & Filters */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex overflow-x-auto pb-2 sm:pb-0 scrollbar-hide gap-2">
          {filters.map(f => (
            <button 
              key={f.id} 
              onClick={() => setFilter(f.id)}
              className={`px-4 py-2 rounded-lg text-sm font-bold whitespace-nowrap transition-colors ${filter === f.id ? 'bg-indigo-500 text-white' : 'bg-slate-800 text-slate-400 hover:bg-slate-700 hover:text-white'}`}
            >
              {f.label}
            </button>
          ))}
        </div>
        <button onClick={refresh} disabled={loading} className="btn-outline !px-4 !py-2 !text-xs shrink-0 self-start sm:self-auto flex items-center gap-2">
          <FiRefreshCw size={14} className={loading ? "animate-spin" : ""} /> Refresh
        </button>
      </div>

      {/* Orders List */}
      {loading ? (
        <div className="space-y-4">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="card p-6 flex items-center justify-between">
              <div className="skeleton h-6 w-32" />
              <div className="skeleton h-8 w-24" />
            </div>
          ))}
        </div>
      ) : filteredOrders.length === 0 ? (
        <EmptyState 
          icon="inbox"
          title="No orders found"
          message={filter === "all" ? "You haven't placed any orders yet. Discover our latest products and find something you'll love." : `You have no ${filter} orders.`}
          actionText="Start Shopping"
          actionLink="/shop"
        />
      ) : (
        <div className="space-y-4">
          {filteredOrders.map(o => (
            <motion.div key={o.id} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="card p-5 sm:p-6 hover:border-indigo-500/30 transition-colors">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div className="flex items-center gap-4 sm:gap-6">
                  <div className="hidden sm:flex w-12 h-12 rounded-full bg-slate-800 items-center justify-center text-slate-400">
                    <FiPackage size={20} />
                  </div>
                  <div>
                    <h3 className="font-black text-white">Order #{o.order_number}</h3>
                    <p className="text-xs text-slate-400 mt-1 flex items-center gap-2">
                      <FiClock size={10} /> {new Date(o.created_at).toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" })}
                      <span className="w-1 h-1 bg-slate-600 rounded-full mx-1"></span>
                      {o.items.length} item{o.items.length !== 1 && 's'}
                    </p>
                  </div>
                </div>
                
                <div className="flex items-center justify-between sm:justify-end gap-6 sm:w-auto w-full">
                  <div className="text-left sm:text-right">
                    <div className="font-black text-white">{formatPrice(Number(o.total_price), userCurrency, rates)}</div>
                    <div className={`text-xs font-bold uppercase tracking-wider mt-1 ${o.status === 'cancelled' ? 'text-red-400' : 'text-indigo-400'}`}>
                      {o.status}
                    </div>
                  </div>
                  <button onClick={() => setSelectedOrder(o)} className="btn-primary !px-5 !py-2 !text-xs shrink-0">
                    View Order
                  </button>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  );
};


// --- MAIN PAGE COMPONENT ---
export default function ProfilePage() {
  const [searchParams, setSearchParams] = useSearchParams();
  const currentTab = searchParams.get("tab") || "account";
  
  const { user } = useSelector((s) => s.auth);
  const userCountry = useSelector(selectCountry);
  const userCurrency = useSelector(selectCurrency);
  const { rates } = useSelector(selectProducts);
  const { orders, loading, refresh } = useFetchOrders();

  const handleCancelOrder = async (orderId) => {
    if (!window.confirm("Are you sure you want to cancel this order?")) return;
    try {
      await api.post(`/orders/${orderId}/cancel/`);
      toast.success("Order cancelled successfully");
      refresh();
    } catch (err) {
      toast.error(err.response?.data?.detail || "Failed to cancel order");
    }
  };

  const setTab = (tabId) => {
    setSearchParams({ tab: tabId });
  };

  return (
    <PageTransition>
      <div className="mx-auto max-w-5xl px-4 py-8 sm:py-12 sm:px-6">
        
        {/* Account Header Summary */}
        <div className="card mb-8 overflow-hidden relative border-none bg-gradient-to-br from-slate-900 to-slate-800 shadow-xl">
          <div className="absolute inset-0 bg-indigo-500/5 pointer-events-none"></div>
          <div className="p-6 sm:p-8 flex flex-col sm:flex-row items-center sm:items-start gap-6 text-center sm:text-left relative z-10">
            <div className="w-20 h-20 sm:w-24 sm:h-24 rounded-full bg-indigo-500 text-3xl font-black text-white flex items-center justify-center shrink-0 shadow-lg shadow-indigo-500/20">
              {user?.username?.slice(0, 2).toUpperCase() ?? "?"}
            </div>
            <div className="flex-1">
              <h1 className="text-2xl sm:text-3xl font-black tracking-tight text-white mb-1">{user?.first_name ? `${user.first_name} ${user.last_name}` : user?.username}</h1>
              <p className="text-slate-400 text-sm mb-4">{user?.email}</p>
              
              <div className="flex flex-wrap items-center justify-center sm:justify-start gap-3 text-xs font-bold">
                <span className="bg-slate-800/80 px-3 py-1.5 rounded-full text-slate-300 flex items-center gap-1.5 border border-slate-700">
                  <FiPackage className="text-indigo-400" /> {orders?.length || 0} Orders
                </span>
                <span className="bg-slate-800/80 px-3 py-1.5 rounded-full text-slate-300 flex items-center gap-1.5 border border-slate-700">
                  <FiUser className="text-indigo-400" /> Member since {new Date().getFullYear()}
                </span>
              </div>
            </div>
            <div className="w-full sm:w-auto">
               <button onClick={() => setTab("account")} className="btn-outline w-full sm:w-auto !py-2">Edit Profile</button>
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="flex items-center gap-2 mb-8 border-b border-slate-800 pb-px">
          <button 
            onClick={() => setTab("account")} 
            className={`flex items-center gap-2 px-6 py-3 font-bold text-sm transition-all border-b-2 ${currentTab === "account" ? "border-indigo-500 text-indigo-400" : "border-transparent text-slate-400 hover:text-slate-200"}`}
          >
            <FiUser size={16} /> My Account
          </button>
          <button 
            onClick={() => setTab("orders")} 
            className={`flex items-center gap-2 px-6 py-3 font-bold text-sm transition-all border-b-2 ${currentTab === "orders" ? "border-indigo-500 text-indigo-400" : "border-transparent text-slate-400 hover:text-slate-200"}`}
          >
            <FiPackage size={16} /> My Orders
          </button>
        </div>

        {/* Content Area */}
        <AnimatePresence mode="wait">
          <motion.div
            key={currentTab}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.2 }}
          >
            {currentTab === "account" && <AccountTab user={user} />}
            {currentTab === "orders" && (
              <OrdersTab 
                orders={orders} 
                loading={loading} 
                refresh={refresh} 
                userCurrency={userCurrency} 
                rates={rates} 
                handleCancelOrder={handleCancelOrder} 
              />
            )}
          </motion.div>
        </AnimatePresence>

      </div>
    </PageTransition>
  );
}


