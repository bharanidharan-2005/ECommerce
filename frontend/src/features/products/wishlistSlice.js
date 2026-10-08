import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import api from "../../api/axios";

export const fetchWishlist = createAsyncThunk(
  "wishlist/fetch",
  async (_, { rejectWithValue }) => {
    try {
      const { data } = await api.get("/products/wishlist/");
      return Array.isArray(data) ? data : (data.results || []);
    } catch (err) {
      return rejectWithValue(err.response?.data || "Failed to fetch wishlist");
    }
  }
);

export const toggleWishlist = createAsyncThunk(
  "wishlist/toggle",
  async (productId, { getState, rejectWithValue }) => {
    try {
      const { items } = getState().wishlist;
      const existing = items.find((item) => String(item.product) === String(productId) || String(item.product?.id) === String(productId) || String(item.product_details?.id) === String(productId));
      
      if (existing) {
        await api.delete(`/products/wishlist/${existing.id}/`);
        return { productId, action: "removed", id: existing.id };
      } else {
        const { data } = await api.post("/products/wishlist/", { product: productId });
        return { action: "added", item: data };
      }
    } catch (err) {
      return rejectWithValue(err.response?.data || "Failed to toggle wishlist");
    }
  }
);

const wishlistSlice = createSlice({
  name: "wishlist",
  initialState: {
    items: [],
    status: "idle",
  },
  reducers: {
    clearWishlist: (state) => {
      state.items = [];
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchWishlist.pending, (state) => {
        state.status = "loading";
      })
      .addCase(fetchWishlist.fulfilled, (state, action) => {
        state.status = "succeeded";
        state.items = action.payload;
      })
      .addCase(fetchWishlist.rejected, (state) => {
        state.status = "failed";
      })
      .addCase(toggleWishlist.fulfilled, (state, action) => {
        if (action.payload.action === "removed") {
          state.items = state.items.filter((item) => item.id !== action.payload.id);
        } else if (action.payload.action === "added") {
          state.items.push(action.payload.item);
        }
      });
  }
});

export const { clearWishlist } = wishlistSlice.actions;
export const selectWishlistItems = (state) => state.wishlist.items;
export default wishlistSlice.reducer;

