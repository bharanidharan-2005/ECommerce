import re

file_path = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\CheckoutPage.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Imports
content = content.replace(
    'import { clearCart, saveShippingAddress, selectCartTotal } from "../features/cart/cartSlice";',
    'import { clearCart, saveShippingAddress, selectCartTotal, applyCoupon, removeCoupon } from "../features/cart/cartSlice";'
)

# 2. Add coupon selector
content = content.replace(
    'const savedAddress = useSelector((s) => s.cart.shippingAddress);',
    'const savedAddress = useSelector((s) => s.cart.shippingAddress);\n  const coupon = useSelector((s) => s.cart.coupon);'
)

# 3. Replace state
old_state = """  const [promoCode, setPromoCode] = useState("");
  const [appliedPromo, setAppliedPromo] = useState(null);
  const [discountPercent, setDiscountPercent] = useState(0);

  const applyPromoCode = async () => {
    if (!promoCode.trim()) return;
    try {
      const { data } = await api.post("/orders/promo/validate/", { code: promoCode });
      setAppliedPromo(data.code);
      setDiscountPercent(data.discount_percentage);
      toast.success(`Promo code applied! ${data.discount_percentage}% off`);
    } catch (err) {
      toast.error(err.response?.data?.detail || "Invalid promo code");
      setAppliedPromo(null);
      setDiscountPercent(0);
    }
  };"""

new_state = """  const [promoCode, setPromoCode] = useState("");
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
  };"""

content = content.replace(old_state, new_state)

# 4. discountedTotal calculation
content = content.replace(
    'const discountedTotal = total * (1 - (discountPercent / 100));',
    'const discountPercent = coupon ? coupon.discount_percentage : 0;\n  const discountedTotal = total * (1 - (discountPercent / 100));'
)

# 5. UI Updates
old_ui = """                    <div className="pt-3 border-t border-slate-700 flex justify-between items-center">
                      <span className="font-bold text-slate-200">Total</span>
                      <span className="text-xl font-black text-indigo-400">{convertedTotal}</span>
                    </div>"""

new_ui = """                    {coupon && (
                      <div className="flex justify-between items-center text-emerald-400">
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
                    <div className="pt-3 border-t border-slate-700 flex justify-between items-center">
                      <span className="font-bold text-slate-200">Total</span>
                      <span className="text-xl font-black text-indigo-400">{convertedTotal}</span>
                    </div>"""

content = content.replace(old_ui, new_ui)

# 6. Make sure to use the correct promo variable in checkout submit
content = content.replace(
    'promo_code: appliedPromo',
    'promo_code: coupon ? coupon.code : null'
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated CheckoutPage.jsx")
