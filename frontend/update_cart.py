import re

file_path = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\features\cart\cartSlice.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add coupon to initial state
content = content.replace(
    'paymentMethod: "stripe",\n  },',
    'paymentMethod: "stripe",\n    coupon: null,\n  },'
)

# Add applyCoupon and removeCoupon actions
reducers_addition = """
    applyCoupon(state, action) {
      if (action.payload === "WELCOME10") {
        state.coupon = "WELCOME10";
        toast.success("Coupon WELCOME10 applied! 10% discount.");
      } else {
        toast.error("Invalid coupon code");
      }
    },
    removeCoupon(state) {
      state.coupon = null;
      toast.info("Coupon removed");
    },
"""

content = content.replace(
    'clearCart(state) {',
    reducers_addition + '    clearCart(state) {'
)

# Add to exports
content = content.replace(
    'clearCart,',
    'applyCoupon,\n  removeCoupon,\n  clearCart,'
)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated cartSlice.js")
