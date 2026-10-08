import re

file_path = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\CheckoutPage.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

pattern = re.compile(r'(<div className="pt-3 border-t border-slate-700 flex justify-between items-center">\s*<span className="font-bold text-slate-200">Total</span>\s*<span className="text-xl font-black text-indigo-400">\{convertedTotal\}</span>\s*</div>)')

new_ui = """                    {coupon && (
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
                          placeholder="Promo code (e.g. WELCOME10)" 
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
                    \\1"""

if pattern.search(content):
    content = pattern.sub(new_ui, content)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated CheckoutPage.jsx UI via Regex")
else:
    print("pattern not found")
