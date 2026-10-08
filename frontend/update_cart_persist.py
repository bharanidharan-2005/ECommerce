import re

file_path = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\features\cart\cartSlice.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Make initial state use localStorage
content = content.replace(
    'coupon: null,',
    'coupon: JSON.parse(localStorage.getItem("cartCoupon") || "null"),'
)

# Make applyCoupon save to localStorage
old_apply = """    applyCoupon(state, action) {
      state.coupon = action.payload; // { code: 'WELCOME10', discount_percentage: 10 }
    },"""
new_apply = """    applyCoupon(state, action) {
      state.coupon = action.payload; // { code: 'WELCOME10', discount_percentage: 10 }
      localStorage.setItem("cartCoupon", JSON.stringify(action.payload));
    },"""
content = content.replace(old_apply, new_apply)

# Make removeCoupon remove from localStorage
old_remove = """    removeCoupon(state) {
      state.coupon = null;
      toast.info("Coupon removed");
    },"""
new_remove = """    removeCoupon(state) {
      state.coupon = null;
      localStorage.removeItem("cartCoupon");
      toast.info("Coupon removed");
    },"""
content = content.replace(old_remove, new_remove)

# clearCart should also remove coupon
old_clear = """    clearCart(state) {
      state.items = [];
      save([]);
    },"""
new_clear = """    clearCart(state) {
      state.items = [];
      state.coupon = null;
      save([]);
      localStorage.removeItem("cartCoupon");
    },"""
content = content.replace(old_clear, new_clear)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated cartSlice persistence")
