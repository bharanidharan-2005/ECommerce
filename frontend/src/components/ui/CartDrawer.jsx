import React, { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { AnimatePresence, motion } from "framer-motion";
import * as Dialog from "@radix-ui/react-dialog";
import { Link, useNavigate } from "react-router-dom";
import { FiMinus, FiPlus, FiShoppingBag, FiX, FiArrowRight } from "react-icons/fi";

import {
  removeFromCart,
  selectCartTotal,
  applyCoupon,
  removeCoupon,
  updateQty,
} from "../../features/cart/cartSlice";
import { closeCart, selectCurrency } from "../../features/ui/uiSlice";
import api from "../../api/axios";
import { toast } from "react-toastify";
import { useState } from "react";
import { formatPrice, selectProducts } from "../../features/products/productsSlice";

const mediaUrl = (path) => {
  if (!path) return "";
  if (/^https?:\/\//i.test(path) || path.startsWith('data:image')) return path;
  const base = (import.meta.env.VITE_API_URL || "http://localhost:8010/api").replace(/\/api$/, "");
  return `${base}${path}`;
};

const FREE_SHIPPING_AT_INR = 1500;

export default function CartDrawer() {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const open = useSelector((s) => s.ui.cartOpen);
  const items = useSelector((s) => s.cart.items);
  const total = useSelector(selectCartTotal);
  const currency = useSelector(selectCurrency);
  const { rates } = useSelector(selectProducts);
  const coupon = useSelector((s) => s.cart.coupon);
  const [promoCode, setPromoCode] = useState("");
  const [validatingPromo, setValidatingPromo] = useState(false);

  const handleApplyPromo = async () => {
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

  useEffect(() => {
    document.body.style.overflow = open ? "hidden" : "";
    return () => {
      document.body.style.overflow = "";
    };
  }, [open]);

  const goToCheckout = () => {
    dispatch(closeCart());
    navigate("/checkout");
  };

  const discount = coupon ? (total * coupon.discount_percentage) / 100 : 0;
  const finalTotal = total - discount;
  
  const shippingProgress = Math.min((total / FREE_SHIPPING_AT_INR) * 100, 100);

  return (
    <Dialog.Root open={open} onOpenChange={(isOpen) => !isOpen && dispatch(closeCart())}>
      <AnimatePresence>
        {open && (
          <Dialog.Portal forceMount>
            <Dialog.Overlay asChild forceMount>
              <motion.div
                className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.2 }}
              />
            </Dialog.Overlay>

            <Dialog.Content asChild forceMount>
              <motion.div
                className="fixed inset-y-0 right-0 z-50 flex w-full max-w-md flex-col bg-slate-900 shadow-2xl outline-none border-l border-slate-800"
                initial={{ x: "100%" }}
                animate={{ x: 0 }}
                exit={{ x: "100%" }}
                transition={{ type: "spring", stiffness: 320, damping: 32 }}
                aria-describedby={undefined}
              >
                {/* Header */}
                <div className="flex items-center justify-between border-b border-slate-800 px-6 py-5 bg-slate-900/95 sticky top-0 z-10">
                  <Dialog.Title className="flex items-center gap-2 text-lg font-extrabold tracking-tight text-white">
                    <FiShoppingBag className="text-indigo-400" />
                    Cart <span className="text-slate-400 font-medium text-sm">({items.reduce((n, i) => n + i.qty, 0)})</span>
                  </Dialog.Title>
                  <Dialog.Close asChild>
                    <button
                      className="rounded-full p-2 text-slate-400 transition hover:bg-slate-800 hover:text-white"
                      aria-label="Close cart"
                    >
                      <FiX size={20} />
                    </button>
                  </Dialog.Close>
                </div>

                {/* Free shipping progress */}
                {items.length > 0 && total < FREE_SHIPPING_AT_INR && (
                  <div className="border-b border-slate-800 bg-slate-800/30 px-6 py-4">
                    <p className="mb-2 text-sm font-medium text-slate-300">
                      You're <span className="font-bold text-indigo-400">{formatPrice(FREE_SHIPPING_AT_INR - total, currency)}</span> away from free shipping!
                    </p>
                    <div className="h-1.5 overflow-hidden rounded-full bg-slate-700">
                      <motion.div
                        className="h-full rounded-full bg-indigo-500"
                        initial={{ width: 0 }}
                        animate={{ width: `${shippingProgress}%` }}
                        transition={{ type: "spring", stiffness: 120, damping: 20 }}
                      />
                    </div>
                  </div>
                )}
                {items.length > 0 && total >= FREE_SHIPPING_AT_INR && (
                   <div className="border-b border-slate-800 bg-emerald-500/10 px-6 py-3">
                     <p className="text-sm font-medium text-emerald-400 flex items-center justify-center">
                       You've unlocked free shipping!
                     </p>
                   </div>
                )}

                {/* Line items */}
                <div className="flex-1 overflow-y-auto px-6 py-4">
                  {items.length === 0 ? (
                    <EmptyState onClose={() => dispatch(closeCart())} />
                  ) : (
                    <ul className="flex flex-col gap-4 py-1">
                      <AnimatePresence initial={false}>
                        {items.map((item) => (
                          <motion.li
                            key={item.id}
                            layout
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, x: 40 }}
                            transition={{ duration: 0.22 }}
                            className="flex gap-4 rounded-xl border border-slate-800 bg-slate-800/50 p-3 shadow-sm relative pr-10"
                          >
                            <img
                              src={mediaUrl(item.image)}
                              alt={item.name}
                              className="h-20 w-20 flex-shrink-0 rounded-lg object-contain bg-slate-800"
                            />
                            <div className="flex min-w-0 flex-1 flex-col">
                              <p className="truncate text-sm font-bold text-white mb-1">{item.name}</p>
                              <p className="text-sm text-indigo-400 font-semibold">{formatPrice(Number(item.price), currency)}</p>

                              {/* Quantity stepper */}
                              <div className="mt-auto flex items-center justify-between pt-2">
                                <div className="flex items-center rounded-lg border border-slate-700 bg-slate-800">
                                  <button
                                    onClick={() => dispatch(updateQty({ id: item.id, qty: item.qty - 1 }))}
                                    className="p-1.5 text-slate-400 transition hover:text-white disabled:opacity-30"
                                    disabled={item.qty <= 1}
                                  >
                                    <FiMinus size={14} />
                                  </button>
                                  <span className="w-8 text-center text-sm font-bold text-white">{item.qty}</span>
                                  <button
                                    onClick={() => dispatch(updateQty({ id: item.id, qty: item.qty + 1 }))}
                                    className="p-1.5 text-slate-400 transition hover:text-white"
                                  >
                                    <FiPlus size={14} />
                                  </button>
                                </div>
                                <span className="text-sm font-extrabold text-white">
                                  {formatPrice(Number(item.price) * item.qty, currency)}
                                </span>
                              </div>
                            </div>

                            <button
                              onClick={() => dispatch(removeFromCart(item.id))}
                              className="absolute top-3 right-3 rounded-full p-1.5 text-slate-500 transition hover:bg-slate-700 hover:text-rose-400"
                              aria-label={`Remove ${item.name} from cart`}
                            >
                              <FiX size={16} />
                            </button>
                          </motion.li>
                        ))}
                      </AnimatePresence>
                    </ul>
                  )}
                </div>

                {/* Order summary + CTA */}
                {items.length > 0 && (
                  <div className="border-t border-slate-800 bg-slate-900 px-6 py-6 sticky bottom-0 z-10 shadow-[0_-10px_20px_-10px_rgba(0,0,0,0.5)]">
                    <dl className="mb-6 space-y-2.5 text-sm">
                      <div className="flex justify-between text-slate-300">
                        <dt>Subtotal</dt>
                        <dd className="font-medium text-white">{formatPrice(total, currency)}</dd>
                      </div>
                      <div className="flex justify-between text-slate-300">
                        <dt>Shipping</dt>
                        <dd className="font-medium text-white">{shippingCost === 0 ? "Free" : formatPrice(shippingCost, currency)}</dd>
                      </div>
                      <div className="flex justify-between text-slate-300">
                        <dt>Tax (Estimated)</dt>
                        <dd className="font-medium text-white">{formatPrice(tax, currency)}</dd>
                      </div>
                      {coupon && (
                        <div className="flex justify-between items-center text-emerald-400 bg-emerald-500/10 px-3 py-2 rounded-lg border border-emerald-500/20 -mx-3">
                          <dt className="flex items-center gap-2">
                            <span className="font-bold text-xs uppercase tracking-wider">{coupon.code}</span>
                            <span className="text-xs">(-{coupon.discount_percentage}%)</span>
                          </dt>
                          <dd className="font-medium flex items-center gap-3">
                            -{formatPrice(discount, currency)}
                            <button onClick={() => dispatch(removeCoupon())} className="text-emerald-500 hover:text-rose-400"><FiX size={14} /></button>
                          </dd>
                        </div>
                      )}
                      {!coupon && (
                        <div className="flex gap-2 -mx-3 pt-2">
                          <input 
                            type="text" 
                            placeholder="Promo code (e.g. bharani10)" 
                            value={promoCode}
                            onChange={(e) => setPromoCode(e.target.value.toUpperCase())}
                            className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-indigo-500"
                          />
                          <button 
                            onClick={handleApplyPromo}
                            disabled={validatingPromo || !promoCode}
                            className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg text-sm font-bold transition disabled:opacity-50"
                          >
                            Apply
                          </button>
                        </div>
                      )}
                      <div className="flex justify-between border-t border-slate-800 pt-3 text-base font-extrabold text-white">
                        <dt>Total</dt>
                        <dd>{formatPrice(finalTotal, currency)}</dd>
                      </div>
                    </dl>
                    
                    <button onClick={goToCheckout} className="flex w-full items-center justify-center gap-2 rounded-full bg-indigo-600 px-6 py-3.5 text-base font-bold text-white transition hover:bg-indigo-700 shadow-lg shadow-indigo-900/20">
                      Proceed to Checkout <FiArrowRight />
                    </button>
                    
                    <button onClick={() => dispatch(closeCart())} className="mt-4 flex w-full items-center justify-center text-sm font-medium text-slate-400 transition hover:text-white">
                      Continue Shopping
                    </button>
                  </div>
                )}
              </motion.div>
            </Dialog.Content>
          </Dialog.Portal>
        )}
      </AnimatePresence>
    </Dialog.Root>
  );
}

function EmptyState({ onClose }) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.96 }}
      animate={{ opacity: 1, scale: 1 }}
      className="flex h-full flex-col items-center justify-center gap-4 pb-16 text-center"
    >
      <div className="flex h-20 w-20 items-center justify-center rounded-full bg-slate-800 text-slate-400">
        <FiShoppingBag size={32} />
      </div>
      <div>
        <p className="text-lg font-extrabold text-white">Your cart is empty.</p>
        <p className="mt-2 text-sm text-slate-400 max-w-[240px] mx-auto">
          Explore the collection and add something you love.
        </p>
      </div>
      <Link to="/products" onClick={onClose} className="mt-4 inline-flex items-center justify-center gap-2 rounded-full bg-slate-800 px-6 py-3 text-sm font-bold text-white transition hover:bg-slate-700">
        Explore Products <FiArrowRight />
      </Link>
    </motion.div>
  );
}
