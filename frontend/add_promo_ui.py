import os

filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\CheckoutPage.jsx"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# 1. State hooks
old_state = """  const [processing, setProcessing] = useState(false);"""
new_state = """  const [processing, setProcessing] = useState(false);
  const [promoCode, setPromoCode] = useState("");
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
content = content.replace(old_state, new_state)

# 2. placeOrder payload
old_payload = """          payment_method: method,
          upi_id: method.startsWith("upi_") ? upiId : "",
          items: items.map((i) => ({ product_id: i.id, quantity: i.qty })),
        });"""
new_payload = """          payment_method: method,
          upi_id: method.startsWith("upi_") ? upiId : "",
          promo_code: appliedPromo,
          items: items.map((i) => ({ product_id: i.id, quantity: i.qty })),
        });"""
content = content.replace(old_payload, new_payload)

# 3. Calculate discounted total
old_total_calc = """  const convertedTotal = formatPrice(total, currency, rates);"""
new_total_calc = """  const discountedTotal = total * (1 - (discountPercent / 100));
  const convertedTotal = formatPrice(discountedTotal, currency, rates);"""
content = content.replace(old_total_calc, new_total_calc)

# 4. Render promo input in step 3
old_summary_header = """                <div className="bg-slate-800/30 p-4 rounded-xl border border-slate-800">
                  <h3 className="text-sm font-bold text-slate-300 uppercase tracking-wider mb-3">Order Summary</h3>
                  <div className="space-y-3">"""

new_summary_header = """                <div className="bg-slate-800/30 p-4 rounded-xl border border-slate-800">
                  <div className="flex justify-between items-center mb-3">
                    <h3 className="text-sm font-bold text-slate-300 uppercase tracking-wider">Order Summary</h3>
                  </div>
                  
                  <div className="mb-4 flex gap-2">
                    <input 
                      type="text" 
                      placeholder="Promo Code" 
                      className="input flex-1 bg-slate-900 border-slate-700 text-sm uppercase"
                      value={promoCode}
                      onChange={(e) => setPromoCode(e.target.value)}
                      disabled={!!appliedPromo}
                    />
                    <button 
                      type="button"
                      onClick={appliedPromo ? () => { setAppliedPromo(null); setDiscountPercent(0); setPromoCode(""); } : applyPromoCode}
                      className="btn-outline text-sm px-4 py-2"
                    >
                      {appliedPromo ? "Remove" : "Apply"}
                    </button>
                  </div>

                  <div className="space-y-3">"""
content = content.replace(old_summary_header, new_summary_header)

# 5. Render discount line
old_total_row = """                    <div className="pt-3 border-t border-slate-700 flex justify-between items-center">
                      <span className="font-bold text-slate-200">Total</span>
                      <span className="text-xl font-black text-indigo-400">{convertedTotal}</span>
                    </div>"""
new_total_row = """                    {discountPercent > 0 && (
                      <div className="flex justify-between items-center text-sm text-emerald-400">
                        <span>Discount ({appliedPromo} - {discountPercent}%)</span>
                        <span>-{formatPrice(total * (discountPercent/100), currency, rates)}</span>
                      </div>
                    )}
                    <div className="pt-3 border-t border-slate-700 flex justify-between items-center">
                      <span className="font-bold text-slate-200">Total</span>
                      <span className="text-xl font-black text-indigo-400">{convertedTotal}</span>
                    </div>"""
content = content.replace(old_total_row, new_total_row)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated CheckoutPage.jsx with promo UI")
