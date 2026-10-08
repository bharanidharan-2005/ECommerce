/**
 * LoginPage — glass card on soft gradient backdrop.
 * Framer Motion entrance + tactile button feedback per the design system.
 * After signing in, honors ?next= so users resume where they left off
 * (e.g. clicking "Track My Order" while signed out).
 */
import { useState } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { motion } from "framer-motion";
import { toast } from "react-toastify";

import PageTransition from "../components/PageTransition.jsx";
import { clearError, login } from "../features/auth/authSlice";

export default function LoginPage() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [params] = useSearchParams();
  const { loading, error } = useSelector((s) => s.auth);

  const [form, setForm] = useState({ email: "", password: "" });

  const submit = async (e) => {
    e.preventDefault();
    dispatch(clearError());
    const res = await dispatch(login(form));
    if (res.meta.requestStatus === "fulfilled") {
      toast.success("Welcome back!");
      // Only follow in-app paths — never open redirects from the query string
      const next = params.get("next");
      navigate(next && next.startsWith("/") ? next : "/");
    }
  };

  return (
    <PageTransition>
      <div className="relative flex min-h-[calc(100vh-8rem)] items-center justify-center overflow-hidden px-4 py-16">
        {/* Decorative gradient blobs (same language as the home hero) */}
        <div aria-hidden className="absolute left-1/2 top-0 h-72 w-72 -translate-x-1/2 rounded-full bg-indigo-200/40 blur-3xl" />

        <motion.div
          initial={{ opacity: 0, y: 24, scale: 0.98 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ duration: 0.45, ease: [0.22, 1, 0.36, 1] }}
          className="card relative w-full max-w-md p-8 sm:p-10"
        >
          <h1 className="text-3xl font-black tracking-tight">Welcome back</h1>
          <p className="mt-1.5 text-sm text-slate-400">Sign in to track orders and check out faster.</p>

          {error && (
            <motion.p
              initial={{ opacity: 0, y: -6 }}
              animate={{ opacity: 1, y: 0 }}
              className="mt-5 rounded-2xl bg-red-50 p-3 text-sm font-medium text-red-600"
            >
              {error}
            </motion.p>
          )}

          <form onSubmit={submit} className="mt-7 flex flex-col gap-4">
            <div>
              <label htmlFor="login-email" className="mb-1.5 block text-xs font-bold uppercase tracking-wider text-slate-400">
                Email
              </label>
              <input
                id="login-email"
                type="email"
                required
                placeholder="you@example.com"
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
                className="input"
              />
            </div>
            <div>
              <label htmlFor="login-password" className="mb-1.5 block text-xs font-bold uppercase tracking-wider text-slate-400">
                Password
              </label>
              <input
                id="login-password"
                type="password"
                required
                placeholder="••••••••"
                value={form.password}
                onChange={(e) => setForm({ ...form, password: e.target.value })}
                className="input"
              />
            </div>
            <button type="submit" disabled={loading} className="btn-primary mt-2 w-full !py-3">
              {loading ? "Signing in…" : "Sign In"}
            </button>
          </form>

          <p className="mt-7 text-center text-sm text-slate-400">
            No account?{" "}
            <Link to="/register" className="font-bold text-indigo-400 hover:text-indigo-700 hover:underline">
              Create one free
            </Link>
          </p>
        </motion.div>
      </div>
    </PageTransition>
  );
}
