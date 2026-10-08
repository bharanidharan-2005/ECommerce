content = '''import { useEffect, useState } from "react";
import api from "../../api";
import { DollarSign, ShoppingBag, Package, Users } from "lucide-react";
import PageTransition from "../../components/PageTransition";

export default function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/orders/admin/stats/")
      .then((res) => {
        setStats(res.data);
      })
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="h-32 animate-pulse rounded-2xl bg-slate-800/50" />
        ))}
      </div>
    );
  }

  const cards = [
    { label: "Total Revenue", value: \$\\, icon: DollarSign, color: "text-emerald-400" },
    { label: "Total Orders", value: stats?.total_orders, icon: ShoppingBag, color: "text-indigo-400" },
    { label: "Total Products", value: stats?.total_products, icon: Package, color: "text-amber-400" },
    { label: "Total Users", value: stats?.total_users, icon: Users, color: "text-rose-400" },
  ];

  return (
    <PageTransition>
      <div className="space-y-6">
        <h1 className="text-2xl font-bold text-slate-100">Overview</h1>
        
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {cards.map((card, i) => {
            const Icon = card.icon;
            return (
              <div
                key={i}
                className="flex items-center gap-4 rounded-2xl border border-slate-800 bg-slate-900/50 p-6 shadow-sm"
              >
                <div className={\ounded-full bg-slate-800 p-3 \\}>
                  <Icon className="h-6 w-6" />
                </div>
                <div>
                  <p className="text-sm font-medium text-slate-400">{card.label}</p>
                  <p className="text-2xl font-bold text-slate-100">{card.value}</p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </PageTransition>
  );
}
'''
with open('src/pages/admin/AdminDashboard.jsx', 'w') as f:
    f.write(content)
