/**
 * uiSlice — global UI state (cart drawer + country + currency).
 * Keeping it in Redux lets any component (Navbar, ProductCard, pages)
 * open/close the dropdown without prop drilling.
 * Preferences are persisted: localStorage for guests, database for logged-in users.
 */
import { createSlice } from "@reduxjs/toolkit";

const stored = {
    country: localStorage.getItem("prefCountry"),
    currency: localStorage.getItem("prefCurrency"),
};

const initialState = {
    /** Whether the slide-out cart drawer is visible */
    cartOpen: false,
    /** Selected ISO country code (e.g. "US", "IN", "GB") */
    country: stored.country || "US",
    /** Selected ISO currency code (e.g. "USD", "EUR", "INR") */
    currency: stored.currency || "USD",
};

const uiSlice = createSlice({
    name: "ui",
    initialState,
    reducers: {
        openCart(state) {
            state.cartOpen = true;
        },
        closeCart(state) {
            state.cartOpen = false;
        },
        setCountry(state, action) {
            state.country = action.payload;
            localStorage.setItem("prefCountry", action.payload);
        },
        setCurrency(state, action) {
            state.currency = action.payload;
            localStorage.setItem("prefCurrency", action.payload);
        },
    },
});

export const { openCart, closeCart, setCountry, setCurrency } = uiSlice.actions;

// --- FIX: Added the missing selectors here ---
export const selectCurrency = (state) => state.ui.currency;
export const selectCountry = (state) => state.ui.country;
export const selectCartOpen = (state) => state.ui.cartOpen;

export default uiSlice.reducer;