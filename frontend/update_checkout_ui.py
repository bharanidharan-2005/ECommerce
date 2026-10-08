import re

file_path = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\CheckoutPage.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_ui = """                    <div className="pt-3 border-t border-slate-700 flex justify-between items-center">
                      <span className="font-bold text-slate-200">Total</span>
                      <span className="text-xl font-black text-indigo-400">{convertedTotal}</span>
                    </div>"""

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
                      <div className="flex gap-2 pt-2">
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
                    <div className="pt-3 border-t border-slate-700 flex justify-between items-center">
                      <span className="font-bold text-slate-200">Total</span>
                      <span className="text-xl font-black text-indigo-400">{convertedTotal}</span>
                    </div>"""

if old_ui in content:
    content = content.replace(old_ui, new_ui)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated CheckoutPage.jsx UI")
else:
    print("old_ui not found")
    
# Wait, I also need to make sure handleApplyPromoCode doesn't have an event parameter issue. 
# Also need to import FiX.
if 'import { FiCreditCard, FiMapPin, FiSmartphone, FiCheck, FiArrowRight, FiArrowLeft, FiPackage } from "react-icons/fi";' in content:
    content = content.replace(
        'import { FiCreditCard, FiMapPin, FiSmartphone, FiCheck, FiArrowRight, FiArrowLeft, FiPackage } from "react-icons/fi";',
        'import { FiCreditCard, FiMapPin, FiSmartphone, FiCheck, FiArrowRight, FiArrowLeft, FiPackage, FiX } from "react-icons/fi";'
    )
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

