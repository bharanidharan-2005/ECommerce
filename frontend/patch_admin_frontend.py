import os
import re

# 1. AdminSubscribers.jsx
sub_file = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\admin\AdminSubscribers.jsx'
sub_code = '''import { useState, useEffect } from "react";
import api from "../../api/axios";
import { format } from "date-fns";
import { Mail, CheckCircle, XCircle } from "lucide-react";

export default function AdminSubscribers() {
  const [subscribers, setSubscribers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSubscribers();
  }, []);

  const fetchSubscribers = async () => {
    try {
      const { data } = await api.get("/auth/admin-subscribers/");
      setSubscribers(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const total = subscribers.length;
  const active = subscribers.filter(s => s.is_active).length;
  const couponsUsed = subscribers.filter(s => s.coupon_used).length;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
          <Mail className="h-6 w-6 text-indigo-400" />
          Newsletter Subscribers
        </h1>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-xl">
          <div className="text-sm text-slate-400 font-semibold mb-1">Total Subscribers</div>
          <div className="text-2xl font-black text-white">{total}</div>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-xl">
          <div className="text-sm text-slate-400 font-semibold mb-1">Active Subscribers</div>
          <div className="text-2xl font-black text-emerald-400">{active}</div>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-xl">
          <div className="text-sm text-slate-400 font-semibold mb-1">Coupons Issued</div>
          <div className="text-2xl font-black text-indigo-400">{subscribers.filter(s => s.welcome_coupon).length}</div>
        </div>
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-xl">
          <div className="text-sm text-slate-400 font-semibold mb-1">Coupons Used</div>
          <div className="text-2xl font-black text-white">{couponsUsed}</div>
        </div>
      </div>

      <div className="overflow-hidden rounded-xl border border-slate-800 bg-slate-900 shadow-xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="border-b border-slate-800 bg-slate-900/50 text-xs uppercase text-slate-300">
              <tr>
                <th className="px-6 py-4 font-semibold">Email</th>
                <th className="px-3 py-4 font-semibold">Subscribed Date</th>
                <th className="px-3 py-4 font-semibold">Coupon</th>
                <th className="px-3 py-4 font-semibold">Coupon Status</th>
                <th className="px-3 py-4 font-semibold">Expiry Date</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {loading ? (
                <tr>
                  <td colSpan="5" className="py-8 text-center text-slate-400">Loading...</td>
                </tr>
              ) : subscribers.map((sub) => (
                <tr key={sub.id} className="hover:bg-slate-800/50 transition-colors text-slate-300">
                  <td className="px-6 py-4 font-medium text-white">{sub.email}</td>
                  <td className="px-3 py-4">{format(new Date(sub.subscribed_at), "dd MMM yyyy")}</td>
                  <td className="px-3 py-4 font-mono text-indigo-400">{sub.welcome_coupon || "-"}</td>
                  <td className="px-3 py-4">
                    {sub.coupon_used ? (
                      <span className="inline-flex items-center gap-1 text-slate-400 text-xs"><CheckCircle size={14}/> Used</span>
                    ) : new Date(sub.coupon_expires_at) < new Date() ? (
                      <span className="inline-flex items-center gap-1 text-rose-400 text-xs"><XCircle size={14}/> Expired</span>
                    ) : sub.welcome_coupon ? (
                      <span className="inline-flex items-center gap-1 text-emerald-400 text-xs"><CheckCircle size={14}/> Active</span>
                    ) : "-"}
                  </td>
                  <td className="px-3 py-4">{sub.coupon_expires_at ? format(new Date(sub.coupon_expires_at), "dd MMM yyyy") : "-"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
'''
with open(sub_file, 'w', encoding='utf-8') as f:
    f.write(sub_code)

# 2. Add to AdminLayout.jsx
layout_path = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\admin\AdminLayout.jsx'
with open(layout_path, 'r', encoding='utf-8') as f:
    layout_content = f.read()

layout_content = layout_content.replace('import { \n  LayoutDashboard, ShoppingBag, Package, Users, BarChart2, \n  Settings, LogOut, Bell, Menu, X\n} from "lucide-react";', 'import { \n  LayoutDashboard, ShoppingBag, Package, Users, BarChart2, \n  Settings, LogOut, Bell, Menu, X, Mail, Tag\n} from "lucide-react";')

old_nav = '''  const navItems = [
    { to: "/admin", icon: LayoutDashboard, label: "Dashboard", end: true },
    { to: "/admin/orders", icon: ShoppingBag, label: "Orders" },
    { to: "/admin/products", icon: Package, label: "Products" },
    { to: "/admin/customers", icon: Users, label: "Customers" },
    { to: "/admin/analytics", icon: BarChart2, label: "Analytics" },
  ];'''
new_nav = '''  const navItems = [
    { to: "/admin", icon: LayoutDashboard, label: "Dashboard", end: true },
    { to: "/admin/orders", icon: ShoppingBag, label: "Orders" },
    { to: "/admin/products", icon: Package, label: "Products" },
    { to: "/admin/customers", icon: Users, label: "Customers" },
    { to: "/admin/subscribers", icon: Mail, label: "Subscribers" },
    { to: "/admin/promos", icon: Tag, label: "Promos" },
    { to: "/admin/analytics", icon: BarChart2, label: "Analytics" },
  ];'''
layout_content = layout_content.replace(old_nav, new_nav)
with open(layout_path, 'w', encoding='utf-8') as f:
    f.write(layout_content)


# 3. Add to App.jsx
app_path = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\App.jsx'
with open(app_path, 'r', encoding='utf-8') as f:
    app_content = f.read()

if 'AdminSubscribers' not in app_content:
    app_content = app_content.replace('import AdminPromos from "./pages/admin/AdminPromos.jsx";', 'import AdminPromos from "./pages/admin/AdminPromos.jsx";\nimport AdminSubscribers from "./pages/admin/AdminSubscribers.jsx";')
    app_content = app_content.replace('<Route path="promos" element={<AdminPromos />} />', '<Route path="promos" element={<AdminPromos />} />\n              <Route path="subscribers" element={<AdminSubscribers />} />')
    with open(app_path, 'w', encoding='utf-8') as f:
        f.write(app_content)

print("Frontend Admin files created and patched.")