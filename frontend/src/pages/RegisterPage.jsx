/**
 * RegisterPage — matches LoginPage's card language; auto-signs the user
 * in after successful registration for a friction-free first experience.
 */
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import { motion } from "framer-motion";
import { toast } from "react-toastify";

import PageTransition from "../components/PageTransition.jsx";
import api from "../api/axios";
import { login } from "../features/auth/authSlice";

export default function RegisterPage() {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({ username: "", email: "", first_name: "", password: "" });

  const submit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await api.post("/auth/register/", form);
      toast.success("Account created — welcome to ShopVerse!");
      await dispatch(login({ email: form.email, password: form.password }));
      navigate("/");
    } catch (err) {
      const msg = Object.values(err.response?.data || {})[0] || "Registration failed";
      toast.error(String(msg));
    } finally {
      setLoading(false);
    }
  };

  return (
    <PageTransition>
      <div className="relative flex min-h-[calc(100vh-8rem)] items-center justify-center overflow-hidden px-4 py-16">
        <div aria-hidden className="absolute left-1/2 top-0 h-72 w-72 -translate-x-1/2 rounded-full bg-violet-200/40 blur-3xl" />

        <motion.div
          initial={{ opacity: 0, y: 24, scale: 0.98 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ duration: 0.45, ease: [0.22, 1, 0.36, 1] }}
          className="card relative w-full max-w-md p-8 sm:p-10"
        >
          <h1 className="text-3xl font-black tracking-tight">Join ShopVerse</h1>
          <p className="mt-1.5 text-sm text-slate-400">One account. Order history, faster checkout.</p>

          <form onSubmit={submit} className="mt-7 flex flex-col gap-4">
            {[
              { id: "reg-username", label: "Username", type: "text", key: "username", ph: "janedoe", required: true },
              { id: "reg-email", label: "Email", type: "email", key: "email", ph: "you@example.com", required: true },
              { id: "reg-firstname", label: "First name", type: "text", key: "first_name", ph: "Jane (optional)", required: false },
            ].map((f) => (
              <div key={f.key}>
                <label htmlFor={f.id} className="mb-1.5 block text-xs font-bold uppercase tracking-wider text-slate-400">
                  {f.label}
                </label>
                <input
                  id={f.id}
                  type={f.type}
                  placeholder={f.ph}
                  required={f.required}
                  value={form[f.key]}
                  onChange={(e) => setForm({ ...form, [f.key]: e.target.value })}
                  className="input"
                />
              </div>
            ))}
            <div>
              <label htmlFor="reg-password" className="mb-1.5 block text-xs font-bold uppercase tracking-wider text-slate-400">
                Password
              </label>
              <input
                id="reg-password"
                type="password"
                minLength={8}
                required
                placeholder="Minimum 8 characters"
                value={form.password}
                onChange={(e) => setForm({ ...form, password: e.target.value })}
                className="input"
              />
            </div>
            <button type="submit" disabled={loading} className="btn-primary mt-2 w-full !py-3">
              {loading ? "Creating account…" : "Create Account"}
            </button>
          </form>

          <p className="mt-7 text-center text-sm text-slate-400">
            Already a member?{" "}
            <Link to="/login" className="font-bold text-indigo-400 hover:text-indigo-700 hover:underline">
              Sign in
            </Link>
          </p>
        </motion.div>
      </div>
    </PageTransition>
  );
}
