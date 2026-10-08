import re

file_path = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\components\Footer.jsx"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add imports
content = content.replace(
    'import { Link } from "react-router-dom";',
    'import { Link } from "react-router-dom";\nimport { useDispatch } from "react-redux";\nimport { applyCoupon } from "../features/cart/cartSlice";'
)

# Add dispatch
content = content.replace(
    'export default function Footer() {',
    'export default function Footer() {\n  const dispatch = useDispatch();'
)

# Auto-apply coupon
old_handle = """      setStatus("success");
      setMessage(response.data.message || "Successfully subscribed!");
      setCouponCode(response.data.coupon || "");
      setEmail("");"""

new_handle = """      setStatus("success");
      setMessage(response.data.message || "Successfully subscribed!");
      const coupon = response.data.coupon || "";
      setCouponCode(coupon);
      setEmail("");
      if (coupon) {
        // We know WELCOME10 gives 10% discount in our backend
        dispatch(applyCoupon({ code: coupon, discount_percentage: 10 }));
      }"""

content = content.replace(old_handle, new_handle)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated Footer.jsx")
