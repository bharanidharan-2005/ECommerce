import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import api from "../../api/axios";
import { formatConvertedCurrency } from "../../utils/currency";

export const fetchProducts = createAsyncThunk(
    "products/fetch",
    async({ page = 1, search = "", category = "", ordering = "", min_price = "", max_price = "", in_stock = "", sale = "" }, { rejectWithValue }) => {
        try {
            const params = { page };
            if (search) params.search = search;
            if (category) params.category = category;
            if (ordering) params.ordering = ordering;
            if (min_price) params.min_price = min_price;
            if (max_price) params.max_price = max_price;
            if (in_stock) params.in_stock = "true";
            if (sale) params.sale = "true";
            const { data } = await api.get("/products/", { params });
            return data;
        } catch {
            return rejectWithValue("Failed to load products");
        }
    }
);

export const fetchProduct = createAsyncThunk(
    "products/fetchOne",
    async(id) => {
        const { data } = await api.get(`/products/${id}/`);
        return data;
    }
);

export const fetchExchangeRates = createAsyncThunk(
    "products/fetchExchangeRates",
    async() => {
        const { data } = await api.get("/rates/");
        return data;
    }
);

const formatPrice = (priceInr, currency, rates) => {
  return formatConvertedCurrency(priceInr, "INR", currency || "INR");
};

// Removed the TypeScript "interface RateRecord"

const initialState = {
    items: [],
    count: 0,
    pages: 1,
    current: null,
    loading: false,
    detailLoading: false,
    error: null,
    rates: {}, // Removed the TypeScript "as RateRecord"
};

const productsSlice = createSlice({
    name: "products",
    initialState,
    reducers: {
        setCurrency(state, action) {
            state.currency = action.payload;
        },
        setCountry(state, action) {
            state.country = action.payload;
        },
    },
    extraReducers: (b) => {
        b.addCase(fetchProducts.pending, (s) => {
                s.loading = true;
                s.error = null;
            })
            .addCase(fetchProducts.fulfilled, (s, a) => {
                s.loading = false;
                s.items = a.payload.results;
                s.count = a.payload.count;
                s.pages = Math.ceil(a.payload.count / 12) || 1;
            })
            .addCase(fetchProducts.rejected, (s, a) => {
                s.loading = false;
                s.error = a.payload;
            })
            .addCase(fetchProduct.pending, (s) => {
                s.detailLoading = true;
            })
            .addCase(fetchProduct.fulfilled, (s, a) => {
                s.detailLoading = false;
                s.current = a.payload;
            })
            .addCase(fetchProduct.rejected, (s) => {
                s.detailLoading = false;
            })
            .addCase(fetchExchangeRates.fulfilled, (s, a) => {
                s.rates = a.payload;
            })
            .addCase(fetchExchangeRates.rejected, (s) => {
                s.rates = {};
            });
    },
});

// Added this export so you can dispatch your new actions!
export const { setCurrency, setCountry } = productsSlice.actions;

export default productsSlice.reducer;

export { formatPrice };
export const selectProducts = (state) => state.products;


