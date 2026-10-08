import re

file_path = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\CheckoutPage.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_ui = """                    <div className="pt-3 border-t border-slate-700 flex justify-between items-center">
                      <span className="font-bold text-slate-200">Total</span>
                      <span className="text-xl font-black text-indigo-400">{convertedTotal}</span>
                    </div>"""

# If the previous replace already happened, we need to match that instead.
# Let's check what's there currently.
