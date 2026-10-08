import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import api from "../../api/axios";

const stored = JSON.parse(localStorage.getItem("auth") || "null");

export const register = createAsyncThunk(
  "auth/register",
  async (payload, { rejectWithValue }) => {
    try {
      const { data } = await api.post("/auth/register/", payload);
      return data;
    } catch (e) {
      return rejectWithValue(e.response?.data || "Registration failed");
    }
  }
);

export const login = createAsyncThunk(
  "auth/login",
  async (payload, { rejectWithValue }) => {
    try {
      const { data } = await api.post("/auth/login/", payload);
      return data;
    } catch (e) {
      return rejectWithValue(e.response?.data?.detail || "Invalid credentials");
    }
  }
);

const authSlice = createSlice({
  name: "auth",
  initialState: {
    user: stored?.user || null,
    access: stored?.access || null,
    refresh: stored?.refresh || null,
    loading: false,
    error: null,
  },
  reducers: {
    logout(state) {
      state.user = state.access = state.refresh = null;
      localStorage.removeItem("auth");
    },
    clearError(state) {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(login.pending, (s) => {
        s.loading = true;
        s.error = null;
      })
      .addCase(login.fulfilled, (s, a) => {
        s.loading = false;
        s.access = a.payload.access;
        s.refresh = a.payload.refresh;
        s.user = a.payload.user;
        localStorage.setItem("auth", JSON.stringify(a.payload));
      })
      .addCase(login.rejected, (s, a) => {
        s.loading = false;
        s.error = a.payload;
      })
      .addCase(register.fulfilled, (s, a) => {
        s.user = a.payload;
      });
  },
});

export const { logout, clearError, updateUser } = authSlice.actions;
export default authSlice.reducer;

