/**
 * CheckoutPage - Multi-step animated checkout flow.
 * Steps: 1. Shipping 2. Payment 3. Review
 */
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { loadStripe } from "@stripe/stripe-js";
import { CardElement, Elements, useElements, useStripe } from "@stripe/react-stripe-js";
import { motion, AnimatePresence } from "framer-motion";
import { QRCodeSVG } from "qrcode.react";
import { FiCreditCard, FiMapPin, FiSmartphone, FiCheck, FiArrowRight, FiArrowLeft, FiPackage, FiX } from "react-icons/fi";
import { toast } from "react-toastify";

import PageTransition from "../components/PageTransition.jsx";
import api from "../api/axios";
import { clearCart, saveShippingAddress, selectCartTotal, applyCoupon, removeCoupon } from "../features/cart/cartSlice";
import { formatPrice, selectProducts } from "../features/products/productsSlice";
import { selectCurrency } from "../features/ui/uiSlice";

const stripePromise = loadStripe(import.meta.env.VITE_STRIPE_PUBLISHABLE_KEY || "");

const PAYMENT_METHODS = [
  { id: "cod", label: "Cash on Delivery", desc: "Pay in cash when your order arrives", badge: "COD", color: "bg-emerald-500", icon: <FiPackage size={18} /> },
  { id: "card", label: "Debit / Credit Card", desc: "Visa, Mastercard, RuPay — secured by Stripe", badge: null, icon: <FiCreditCard size={18} />, color: "bg-indigo-500" },
  { id: "upi_gpay", label: "Google Pay", desc: "Instant UPI transfer to GPay@bank", badge: "GPay", color: "bg-sky-500", icon: <FiSmartphone size={18} /> },
  { id: "upi_paytm", label: "Paytm", desc: "Pay via Paytm UPI or wallet balance", badge: "Paytm", color: "bg-cyan-500", icon: <FiSmartphone size={18} /> },
];

const VPA_RE = /^[\w.\-]{2,}@[a-zA-Z]{2,}$/;

const cardStyle = {
  style: {
    base: { color: "#f8fafc", fontFamily: "Inter, sans-serif", fontSize: "15px", "::placeholder": { color: "#9CA3AF" } },
  },
};

const ADDRESS_FIELDS = [
  { name: "full_name", placeholder: "Full name", required: true, span: true },
  { name: "email", placeholder: "Email", type: "email", required: true, span: false },
  { name: "phone", placeholder: "Phone (optional)", type: "tel", required: false, span: false },
  { name: "address_line_1", placeholder: "Address line 1", required: true, span: true },
  { name: "address_line_2", placeholder: "Address line 2 (optional)", required: false, span: true },
  { name: "city", placeholder: "City", required: true, span: false },
  { name: "state", placeholder: "State", required: true, span: false },
  { name: "postal_code", placeholder: "Postal code", required: true, span: false },
  { name: "country", placeholder: "Country", required: true, span: false },
];

function CheckoutForm() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const stripe = useStripe();
  const elements = useElements();

  const items = useSelector((s) => s.cart.items);
  const total = useSelector(selectCartTotal);
  const currency = useSelector(selectCurrency);
  const { rates } = useSelector(selectProducts);
  const savedAddress = useSelector((s) => s.cart.shippingAddress);
  const coupon = useSelector((s) => s.cart.coupon);

  const [step, setStep] = useState(1);
  const [method, setMethod] = useState("cod");
  const [upiId, setUpiId] = useState("");
  const [address, setAddress] = useState(
    savedAddress || {
      full_name: "", email: "", phone: "", address_line_1: "",
      address_line_2: "", city: "", state: "", postal_code: "",
      country: "USA",
    }
  );
  const [processing, setProcessing] = useState(false);
  const [promoCode, setPromoCode] = useState("");
  const [validatingPromo, setValidatingPromo] = useState(false);

  const handleApplyPromoCode = async () => {
    if (!promoCode.trim()) return;
    setValidatingPromo(true);
    try {
      const { data } = await api.post("/orders/promo/validate/", { code: promoCode });
      dispatch(applyCoupon({ code: data.code, discount_percentage: data.discount_percentage }));
      toast.success(`Promo code applied! ${data.discount_percentage}% off`);
      setPromoCode("");
    } catch (err) {
      toast.error(err.response?.data?.detail || "Invalid promo code");
    } finally {
      setValidatingPromo(false);
    }
  };

  const onChange = (e) => setAddress({ ...address, [e.target.name]: e.target.value });

  const nextStep = () => {
    // Validate address before moving to step 2
    if (step === 1) {
      const requiredFields = ADDRESS_FIELDS.filter(f => f.required).map(f => f.name);
      const isComplete = requiredFields.every(f => address[f]?.trim());
      if (!isComplete) {
        toast.error("Please fill all required fields");
        return;
      }
    }
    // Validate UPI before moving to step 3
    if (step === 2 && method.startsWith("upi_") && upiId.trim() !== "") {
      if (!VPA_RE.test(upiId)) {
        toast.error("Enter a valid UPI ID (e.g., name@okbank) or leave blank to scan QR");
        return;
      }
    }
    setStep(s => Math.min(3, s + 1));
  };
  const prevStep = () => setStep(s => Math.max(1, s - 1));

  const placeOrder = async () => {
    try {
      const { data } = await api.post("/orders/checkout/", {
        ...address,
        payment_method: method,
        upi_id: method.startsWith("upi_") ? upiId : "",
        items: items.map((i) => ({ product_id: i.id, quantity: i.qty })),
        promo_code_str: coupon ? coupon.code : null,
      });
      return data;
    } catch (err) {
      toast.error(err.response?.data?.detail || "Checkout failed.");
      return null;
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (step < 3) return nextStep();

    if (method === "upi_gpay" || method === "upi_paytm") {
      setProcessing(true);
      const data = await placeOrder();
      if (!data) { setProcessing(false); return; }
      dispatch(saveShippingAddress(address));
      dispatch(clearCart());
      toast.success("Order Placed!");
      navigate(`/order-success/${data.order.order_number}?method=${method}`, { state: { orderId: data.order.order_number, total: data.order.total_price } });
      return;
    }

    if (method === "cod") {
      setProcessing(true);
      const data = await placeOrder();
      if (!data) { setProcessing(false); return; }
      dispatch(saveShippingAddress(address));
      dispatch(clearCart());
      toast.success("Order Placed!");
      navigate(`/order-success/${data.order.order_number}?method=${method}`, { state: { orderId: data.order.order_number, total: data.order.total_price } });
      return;
    }

    if (method === "card") {
      if (!stripe || !elements) return;
      setProcessing(true);
      const data = await placeOrder();
      if (!data) { setProcessing(false); return; }

      const cardElem = elements.getElement(CardElement);
      const result = await stripe.confirmCardPayment(data.client_secret, {
        payment_method: {
          card: cardElem,
          billing_details: { name: address.full_name, email: address.email },
        },
      });
      if (result.error) {
        toast.error(result.error.message);
        setProcessing(false);
      } else if (result.paymentIntent.status === "succeeded") {
        dispatch(saveShippingAddress(address));
        dispatch(clearCart());
        toast.success("Payment Successful!");
        navigate(`/order-success/${data.order.order_number}?method=${method}`, { state: { orderId: data.order.order_number, total: data.order.total_price } });
      }
    }
  };

  const discountPercent = coupon ? coupon.discount_percentage : 0;
  const discountedTotal = total * (1 - (discountPercent / 100));
  const convertedTotal = formatPrice(discountedTotal, currency, rates);
  
  const stepVariants = {
    hidden: { opacity: 0, x: 20 },
    visible: { opacity: 1, x: 0, transition: { duration: 0.3 } },
    exit: { opacity: 0, x: -20, transition: { duration: 0.2 } }
  };

  return (
    <div className="mx-auto max-w-3xl">
      {/* Progress Bar */}
      <div className="mb-8 flex justify-between items-center relative">
        <div className="absolute left-0 top-1/2 w-full h-1 bg-slate-800 -z-10 rounded"></div>
        <div className="absolute left-0 top-1/2 h-1 bg-indigo-500 -z-10 rounded transition-all duration-500" style={{ width: `${((step - 1) / 2) * 100}%` }}></div>
        
        {["Shipping", "Payment", "Review"].map((label, i) => (
          <div key={label} className="flex flex-col items-center">
            <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm transition-colors duration-300 ${step > i ? 'bg-indigo-500 text-white' : step === i + 1 ? 'bg-slate-700 text-white border-2 border-indigo-500' : 'bg-slate-800 text-slate-500'}`}>
              {step > i + 1 ? <FiCheck /> : i + 1}
            </div>
            <span className={`text-xs mt-2 font-medium ${step >= i + 1 ? 'text-indigo-400' : 'text-slate-500'}`}>{label}</span>
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit} className="bg-slate-900/80 rounded-2xl border border-slate-800 shadow-xl overflow-hidden p-6 sm:p-8">
        <AnimatePresence mode="wait">
          {step === 1 && (
            <motion.div key="step1" variants={stepVariants} initial="hidden" animate="visible" exit="exit" className="space-y-6">
              <div>
                <h2 className="text-xl font-bold flex items-center gap-2"><FiMapPin className="text-indigo-500" /> Shipping Address</h2>
                <p className="text-sm text-slate-400 mt-1">Where should we deliver your order?</p>
              </div>
              <div className="grid grid-cols-2 gap-4">
                {ADDRESS_FIELDS.map((f) => (
                  <div key={f.name} className={f.span ? "col-span-2" : "col-span-2 sm:col-span-1"}>
                    <input
                      type={f.type || "text"}
                      name={f.name}
                      value={address[f.name]}
                      onChange={onChange}
                      placeholder={f.placeholder}
                      required={f.required}
                      className="input w-full bg-slate-800/50 border-slate-700 focus:bg-slate-800 transition-colors"
                    />
                  </div>
                ))}
              </div>
            </motion.div>
          )}

          {step === 2 && (
            <motion.div key="step2" variants={stepVariants} initial="hidden" animate="visible" exit="exit" className="space-y-6">
              <div>
                <h2 className="text-xl font-bold flex items-center gap-2"><FiCreditCard className="text-indigo-500" /> Payment Method</h2>
                <p className="text-sm text-slate-400 mt-1">Choose how you want to pay</p>
              </div>
              <div className="space-y-3">
                {PAYMENT_METHODS.map((m) => (
                  <label key={m.id} className={`flex cursor-pointer items-start gap-4 rounded-xl border p-4 transition-all ${method === m.id ? "border-indigo-500 bg-indigo-500/10 shadow-lg shadow-indigo-500/10" : "border-slate-800 bg-slate-800/50 hover:bg-slate-800 hover:border-slate-700"}`}>
                    <input type="radio" name="payment_method" value={m.id} checked={method === m.id} onChange={(e) => setMethod(e.target.value)} className="mt-1 sr-only" />
                    <div className={`flex h-6 w-6 items-center justify-center rounded-full border ${method === m.id ? "border-indigo-500" : "border-slate-600"}`}>
                      {method === m.id && <div className="h-3 w-3 rounded-full bg-indigo-500" />}
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center gap-2">
                        <span className="font-semibold text-slate-200">{m.label}</span>
                        {m.badge && <span className={`rounded px-1.5 py-0.5 text-[10px] font-bold uppercase tracking-wider text-white ${m.color}`}>{m.badge}</span>}
                      </div>
                      <p className="text-sm text-slate-400">{m.desc}</p>
                    </div>
                    <div className="text-slate-400">{m.icon}</div>
                  </label>
                ))}
              </div>
              
              <AnimatePresence>
                {method.startsWith("upi_") && (
                  <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: "auto" }} exit={{ opacity: 0, height: 0 }} className="pt-2">
                    <input type="text" value={upiId} onChange={(e) => setUpiId(e.target.value)} placeholder="Enter UPI ID (optional, or scan QR on next step)" className="input w-full bg-slate-800/50 border-slate-700 focus:bg-slate-800" />
                  </motion.div>
                )}
                {method === "card" && (
                  <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: "auto" }} exit={{ opacity: 0, height: 0 }} className="pt-2">
                    <div className="rounded-xl border border-slate-700 bg-slate-800/50 p-4 shadow-inner">
                      <CardElement options={cardStyle} />
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
          )}

          {step === 3 && (
            <motion.div key="step3" variants={stepVariants} initial="hidden" animate="visible" exit="exit" className="space-y-6">
              <div>
                <h2 className="text-xl font-bold flex items-center gap-2"><FiCheck className="text-emerald-500" /> Review & Pay</h2>
                <p className="text-sm text-slate-400 mt-1">Please confirm your order details</p>
              </div>
              
              <div className="bg-slate-800/30 p-4 rounded-xl border border-slate-800">
                <h3 className="text-sm font-bold text-slate-300 uppercase tracking-wider mb-3">Order Summary</h3>
                <div className="space-y-3">
                  {items.map(i => (
                    <div key={i.id} className="flex justify-between items-center text-sm">
                      <span className="text-slate-400">{i.qty}x {i.name}</span>
                      <span className="font-medium text-slate-200">{formatPrice(i.price * i.qty, currency, rates)}</span>
                    </div>
                  ))}
                                      {coupon && (
                      <div className="flex justify-between items-center text-emerald-400 bg-emerald-500/10 p-3 rounded-lg border border-emerald-500/20">
                        <div className="flex items-center gap-2">
                          <span className="font-bold text-xs uppercase tracking-wider">{coupon.code}</span>
                          <span className="text-xs">(-{coupon.discount_percentage}%)</span>
                        </div>
                        <div className="flex items-center gap-3 font-medium">
                          -{formatPrice(total * (coupon.discount_percentage / 100), currency, rates)}
                          <button onClick={() => dispatch(removeCoupon())} className="text-emerald-500 hover:text-rose-400"><FiX size={14} /></button>
                        </div>
                      </div>
                    )}
                    {!coupon && (
                      <div className="flex gap-2 pt-2 pb-2">
                        <input 
                          type="text" 
                          placeholder="Promo code (e.g. bharani10)" 
                          value={promoCode}
                          onChange={(e) => setPromoCode(e.target.value.toUpperCase())}
                          className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-indigo-500"
                        />
                        <button 
                          type="button"
                          onClick={handleApplyPromoCode}
                          disabled={validatingPromo || !promoCode}
                          className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg text-sm font-bold transition disabled:opacity-50"
                        >
                          Apply
                        </button>
                      </div>
                    )}
                    <div className="pt-3 border-t border-slate-700 flex justify-between items-center">
                    <span className="font-bold text-slate-200">Total</span>
                    <span className="text-xl font-black text-indigo-400">{convertedTotal}</span>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="bg-slate-800/30 p-4 rounded-xl border border-slate-800">
                  <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Deliver To</h3>
                  <p className="text-sm text-slate-300">{address.full_name}<br/>{address.address_line_1}, {address.city}</p>
                </div>
                <div className="bg-slate-800/30 p-4 rounded-xl border border-slate-800">
                  <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Payment</h3>
                  <p className="text-sm text-slate-300">{PAYMENT_METHODS.find(m => m.id === method)?.label}</p>
                  {method.startsWith('upi') && <p className="text-xs text-slate-500">{upiId}</p>}
                </div>
              </div>

              {method.startsWith('upi') && (
                <div className="bg-white p-6 rounded-xl border border-slate-800 flex flex-col items-center justify-center text-center mt-6 shadow-xl relative overflow-hidden">
                  <div className="absolute top-0 left-0 w-full h-1 bg-indigo-500"></div>
                  <h3 className="text-sm font-bold text-slate-800 mb-4">Scan to Pay via {method === 'upi_gpay' ? 'Google Pay' : 'Paytm'}</h3>
                  <div className="bg-white p-2 rounded-2xl border border-slate-200 shadow-sm inline-block">
                    <QRCodeSVG 
                      value={`upi://pay?pa=${import.meta.env.VITE_MERCHANT_UPI_ID || 'success@razorpay'}&pn=${import.meta.env.VITE_MERCHANT_NAME || 'ShopVerse'}&am=${discountedTotal}&cu=INR`}
                      size={180}
                      level={"H"}
                      includeMargin={true}
                      imageSettings={{
                        src: method === 'upi_gpay' ? 'https://upload.wikimedia.org/wikipedia/commons/f/f2/Google_Pay_Logo.svg' : 'https://upload.wikimedia.org/wikipedia/commons/c/cd/Paytm_logo.png',
                        height: 40,
                        width: 40,
                        excavate: true,
                      }}
                    />
                  </div>
                  <p className="text-xs font-medium text-slate-500 mt-4 px-8">Please scan this QR code with your UPI app. Click below after completing payment.</p>
                </div>
              )}
            </motion.div>
          )}
        </AnimatePresence>

        <div className="mt-8 pt-6 border-t border-slate-800 flex justify-between">
          {step > 1 ? (
            <button type="button" onClick={prevStep} className="btn-outline flex items-center gap-2" disabled={processing}>
              <FiArrowLeft /> Back
            </button>
          ) : <div></div>}
          
          <button type="submit" disabled={processing} className="btn-primary flex items-center gap-2 px-8 shadow-lg shadow-indigo-500/20">
            {processing ? "Processing..." : step === 3 ? `Pay ${convertedTotal}` : "Continue"} 
            {!processing && step < 3 && <FiArrowRight />}
          </button>
        </div>
      </form>
    </div>
  );
}

export default function CheckoutPage() {
  const items = useSelector((s) => s.cart.items);
  if (items.length === 0) {
    return (
      <PageTransition>
        <div className="mx-auto max-w-xl py-24 text-center">
          <h2 className="text-3xl font-black tracking-tight">Your cart is empty</h2>
          <p className="mt-4 text-slate-400">Add some products before checking out.</p>
        </div>
      </PageTransition>
    );
  }

  return (
    <PageTransition>
      <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:py-16">
        <h1 className="text-3xl font-black tracking-tight text-center mb-10">Secure Checkout</h1>
        <Elements stripe={stripePromise}>
          <CheckoutForm />
        </Elements>
      </div>
    </PageTransition>
  );
}

