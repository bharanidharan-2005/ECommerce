import re

file_path = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\features\cart\cartSlice.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace applyCoupon
old_apply = """    applyCoupon(state, action) {
      if (action.payload === "WELCOME10") {
        state.coupon = "WELCOME10";
        toast.success("Coupon WELCOME10 applied! 10% discount.");
      } else {
        toast.error("Invalid coupon code");
      }
    },"""

new_apply = """    applyCoupon(state, action) {
      state.coupon = action.payload; // { code: 'WELCOME10', discount_percentage: 10 }
    },"""

content = content.replace(old_apply, new_apply)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated cartSlice.js applyCoupon")
