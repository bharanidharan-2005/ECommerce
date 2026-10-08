content = """
import { useState, useEffect } from "react";
import api from "../../api/axios";
import { DollarSign, Users, ShoppingBag, Package } from "lucide-react";

export default function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await api.get("/orders/admin-stats/");
        setStats(res.data);
      } catch (err) {
        console.error("Failed to load stats", err);
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  if (loading) return <div className="text-center py-12 text-slate-400">Loading...</div>;

  const statCards = [
    { title: "Total Revenue", value: $${stats?.total_revenue || 0}, icon: DollarSign, color: "text-emerald-500", bg: "bg-emerald-500/10" },
    { title: "Total Orders", value: stats?.total_orders || 0, icon: ShoppingBag, color: "text-blue-500", bg: "bg-blue-500/10" },
    { title: "Total Products", value: stats?.total_products || 0, icon: Package, color: "text-indigo-500", bg: "bg-indigo-500/10" },
    { title: "Total Users", value: stats?.total_users || 0, icon: Users, color: "text-rose-500", bg: "bg-rose-500/10" },
  ];

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-slate-100">Dashboard Overview</h1>
        <p className="mt-1 text-sm text-slate-400">Welcome back, check what's happening today.</p>
      </div>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {statCards.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <div 
              key={index} 
              className="overflow-hidden rounded-xl border border-slate-800 bg-slate-900/50 p-6"
            >
              <div className="flex items-center gap-4">
                <div className={lex h-12 w-12 items-center justify-center rounded-lg }>
                  <Icon className={h-6 w-6 } />
                </div>
                <div>
                  <p className="text-sm font-medium text-slate-400">{stat.title}</p>
                  <p className="mt-1 text-2xl font-semibold text-slate-100">{stat.value}</p>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
"""

with open("src/pages/admin/AdminDashboard.jsx", "w", encoding="utf-8") as f:
    f.write(content.strip())
