import re

file_path = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\components\ui\CartDrawer.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Imports
content = content.replace(
    'removeFromCart,\n  selectCartTotal,',
    'removeFromCart,\n  selectCartTotal,\n  applyCoupon,\n  removeCoupon,'
)
content = content.replace(
    'import { closeCart, selectCurrency } from "../../features/ui/uiSlice";',
    'import { closeCart, selectCurrency } from "../../features/ui/uiSlice";\nimport api from "../../api/axios";\nimport { toast } from "react-toastify";\nimport { useState } from "react";'
)

# 2. Hooks and State
old_hooks = """  const total = useSelector(selectCartTotal);
  const currency = useSelector(selectCurrency);
  const { rates } = useSelector(selectProducts);"""

new_hooks = """  const total = useSelector(selectCartTotal);
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
  };"""

content = content.replace(old_hooks, new_hooks)

# 3. Discount logic
old_discount = """  const tax = total * 0.05; // 5% tax example
  const discount = 0; // Or based on promos
  const finalTotal = total + shippingCost + tax - discount;"""

new_discount = """  const tax = total * 0.05; // 5% tax example
  const discount = coupon ? (total * coupon.discount_percentage) / 100 : 0;
  const finalTotal = total + shippingCost + tax - discount;"""

content = content.replace(old_discount, new_discount)

# 4. JSX
old_jsx = """                      {discount > 0 && (
                        <div className="flex justify-between text-emerald-400">
                          <dt>Discount</dt>
                          <dd className="font-medium">-{formatPrice(discount, "INR", rates)}</dd>
                        </div>
                      )}"""

new_jsx = """                      {coupon && (
                        <div className="flex justify-between items-center text-emerald-400 bg-emerald-500/10 px-3 py-2 rounded-lg border border-emerald-500/20 -mx-3">
                          <dt className="flex items-center gap-2">
                            <span className="font-bold text-xs uppercase tracking-wider">{coupon.code}</span>
                            <span className="text-xs">(-{coupon.discount_percentage}%)</span>
                          </dt>
                          <dd className="font-medium flex items-center gap-3">
                            -{formatPrice(discount, "INR", rates)}
                            <button onClick={() => dispatch(removeCoupon())} className="text-emerald-500 hover:text-rose-400"><FiX size={14} /></button>
                          </dd>
                        </div>
                      )}
                      {!coupon && (
                        <div className="flex gap-2 -mx-3 pt-2">
                          <input 
                            type="text" 
                            placeholder="Promo code (e.g. WELCOME10)" 
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
                      )}"""

content = content.replace(old_jsx, new_jsx)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated CartDrawer.jsx")
