import sys

filepath = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\features\products\productsSlice.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

target = '''export const fetchProducts = createAsyncThunk(
    "products/fetch",
    async({ page = 1, search = "", category = "", ordering = "" }, { rejectWithValue }) => {
        try {
            const params = { page };
            if (search) params.search = search;
            if (category) params.category = category;
            if (ordering) params.ordering = ordering;
            const { data } = await api.get("/products/", { params });'''

replacement = '''export const fetchProducts = createAsyncThunk(
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
            const { data } = await api.get("/products/", { params });'''

content = content.replace(target, replacement)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated productsSlice.js')
