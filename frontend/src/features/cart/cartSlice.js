import { createSlice } from "@reduxjs/toolkit";
import { toast } from "react-toastify";
import { selectCurrency } from "../ui/uiSlice";
import { formatPrice } from "../products/productsSlice";

const stored = JSON.parse(localStorage.getItem("cartItems") || "[]");

const save = (items) => localStorage.setItem("cartItems", JSON.stringify(items));

const cartSlice = createSlice({
  name: "cart",
  initialState: {
    items: stored,
    shippingAddress: JSON.parse(localStorage.getItem("shippingAddress") || "null"),
    paymentMethod: "stripe",
    coupon: JSON.parse(localStorage.getItem("cartCoupon") || "null"),
  },
  reducers: {
    addToCart(state, action) {
      const item = action.payload;
      /* Optional `qty` lets the product-detail page add several at once;
         quick-add buttons omit it and default to 1. */
      const amount = Math.max(1, item.qty ?? 1);
      const existing = state.items.find((i) => i.id === item.id);
      if (existing) {
        const room = (item.stock ?? 99) - existing.qty;
        if (room <= 0) {
          toast.warning("Only limited stock available");
          return;
        }
        existing.qty += Math.min(amount, room);
        toast.info(`${item.name} quantity updated`);
      } else {
        state.items.push({ ...item, qty: amount });
        toast.success(`${item.name} added to cart`);
      }
      save(state.items);
    },
    removeFromCart(state, action) {
      state.items = state.items.filter((i) => i.id !== action.payload);
      save(state.items);
      toast.info("Item removed from cart");
    },
    updateQty(state, action) {
      const { id, qty } = action.payload;
      const item = state.items.find((i) => i.id === id);
      if (item) {
        item.qty = Math.max(1, Math.min(qty, item.stock ?? 99));
        save(state.items);
      }
    },
    
    applyCoupon(state, action) {
      state.coupon = action.payload; // { code: 'WELCOME10', discount_percentage: 10 }
      localStorage.setItem("cartCoupon", JSON.stringify(action.payload));
    },
    removeCoupon(state) {
      state.coupon = null;
      localStorage.removeItem("cartCoupon");
      toast.info("Coupon removed");
    },
    clearCart(state) {
      state.items = [];
      state.coupon = null;
      save([]);
      localStorage.removeItem("cartCoupon");
    },
    saveShippingAddress(state, action) {
      state.shippingAddress = action.payload;
      localStorage.setItem("shippingAddress", JSON.stringify(action.payload));
    },
  },
});

export const {
  addToCart,
  removeFromCart,
  updateQty,
  applyCoupon,
  removeCoupon,
  clearCart,
  saveShippingAddress,
} = cartSlice.actions;

export const selectCartCount = (s) =>
  s.cart.items.reduce((n, i) => n + i.qty, 0);
export const selectCartTotal = (s) => {
  const currency = selectCurrency(s);
  return s.cart.items.reduce(
    (t, i) => t + Number(i.price) * i.qty,
    0
  );
};
export const selectCartTotalFormatted = (s) => {
  const currency = selectCurrency(s);
  const total = selectCartTotal(s);
  return formatPrice(total, currency);
};

export default cartSlice.reducer;
