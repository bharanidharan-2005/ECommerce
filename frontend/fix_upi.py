import os

filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\CheckoutPage.jsx"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the validation logic
old_validation = """    // Validate UPI before moving to step 3
    if (step === 2 && method.startsWith("upi_")) {
      if (!VPA_RE.test(upiId)) {
        toast.error("Enter a valid UPI ID (e.g., name@okbank)");
        return;
      }
    }"""
new_validation = """    // Validate UPI before moving to step 3
    if (step === 2 && method.startsWith("upi_") && upiId.trim() !== "") {
      if (!VPA_RE.test(upiId)) {
        toast.error("Enter a valid UPI ID (e.g., name@okbank) or leave blank to scan QR");
        return;
      }
    }"""
content = content.replace(old_validation, new_validation)

# 2. Update the input element
old_input = """<input type="text" value={upiId} onChange={(e) => setUpiId(e.target.value)} placeholder="Enter UPI ID (e.g., example@okbank)" className="input w-full bg-slate-800/50 border-slate-700 focus:bg-slate-800" required />"""
new_input = """<input type="text" value={upiId} onChange={(e) => setUpiId(e.target.value)} placeholder="Enter UPI ID (optional, or scan QR on next step)" className="input w-full bg-slate-800/50 border-slate-700 focus:bg-slate-800" />"""
content = content.replace(old_input, new_input)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated UPI ID to be optional")
