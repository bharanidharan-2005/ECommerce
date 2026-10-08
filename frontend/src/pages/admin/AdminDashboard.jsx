import React, { useState, useEffect } from "react";
import { IndianRupee, Users, ShoppingBag, TrendingUp, Package, Clock, CheckCircle, XCircle, Settings } from "lucide-react";
import { Link } from "react-router-dom";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from "recharts";

import api from "../../api/axios";
import { formatConvertedCurrency } from "../../utils/currency";

export default function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const [recentOrders, setRecentOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [periodDays, setPeriodDays] = useState(7);
  const [periodLabel, setPeriodLabel] = useState("Last 7 Days");

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        const [statsRes, ordersRes] = await Promise.all([
          api.get(`/orders/admin/stats/?days=${periodDays}`),
          api.get("/orders/admin/?limit=5")
        ]);
        const statsData = statsRes.data;
        if (statsData.sales_data) {
          statsData.sales_data = statsData.sales_data.map(item => ({
            ...item,
            revenue: parseFloat((item.revenue * 96.10).toFixed(2))
          }));
        }
        setStats(statsData);
        setRecentOrders(ordersRes.data.results || []);
      } catch (err) {
        console.error("Failed to load dashboard data");
      } finally {
        setLoading(false);
      }
    };
    fetchDashboardData();
  }, [periodDays]);

  if (loading && !stats) {
    return <div className="text-slate-400 p-8">Loading dashboard...</div>;
  }

  // Assuming conversion rate logic based on users
  
  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between sm:items-center gap-4">
        <h1 className="text-2xl font-bold text-slate-100">Dashboard Overview</h1>
        <div className="flex gap-2">
          <select 
            className="rounded-lg border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-slate-200 focus:border-indigo-500 focus:outline-none"
            value={periodDays}
            onChange={(e) => {
                const val = parseInt(e.target.value);
                setPeriodDays(val);
                if (val === 7) setPeriodLabel("Last 7 Days");
                else if (val === 30) setPeriodLabel("Last 30 Days");
                else setPeriodLabel("This Year");
            }}
          >
            <option value={7}>Last 7 Days</option>
            <option value={30}>Last 30 Days</option>
            <option value={365}>This Year</option>
          </select>
          <button onClick={() => {
            if (!stats?.sales_data?.length) {
              return;
            }
            const headers = ["Date", "Orders", "Revenue (USD)", "Paid", "Delivered", "Pending"];
            const csvContent = [
              headers.join(","),
              ...stats.sales_data.map(row => `${row.date},${row.orders},${row.revenue},${row.paid || 0},${row.delivered || 0},${row.pending || 0}`)
            ].join("\n");
            
            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement("a");
            const url = URL.createObjectURL(blob);
            link.setAttribute("href", url);
            link.setAttribute("download", `dashboard_report.csv`);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
          }} className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-indigo-700">
            Download Report
          </button>
        </div>
      </div>

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {[
          { title: "Total Revenue", value: formatConvertedCurrency(stats?.total_revenue || 0), trend: "+12.5%", icon: IndianRupee, color: "text-emerald-400" },
          { title: "Active Users", value: stats?.total_users || 0, trend: "+5.2%", icon: Users, color: "text-blue-400" },
          { title: "Total Products", value: stats?.total_products || 0, trend: "In Catalog", icon: Package, color: "text-rose-400" },
          { title: "Total Orders", value: stats?.total_orders || 0, trend: "+8.4%", icon: ShoppingBag, color: "text-indigo-400" },
        ].map((stat, i) => (
          <div key={i} className="rounded-xl border border-slate-800 bg-slate-900 p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-slate-400">{stat.title}</p>
                <p className="mt-2 text-2xl font-semibold text-slate-100">{stat.value}</p>
              </div>
              <div className={`rounded-xl bg-slate-800/50 p-3 ${stat.color}`}>
                <stat.icon className="h-6 w-6" />
              </div>
            </div>
            <div className="mt-4 flex items-center gap-2 text-sm">
              <span className={stat.trend.startsWith('+') ? 'text-emerald-400' : 'text-rose-400'}>
                {stat.trend}
              </span>
              <span className="text-slate-500">vs last period</span>
            </div>
          </div>
        ))}
      </div>

      
      {/* Analytics Chart Section */}
      <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">
        <h2 className="text-lg font-semibold text-slate-100 mb-6">Revenue Trend ({periodLabel})</h2>
        <div className="h-72 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={stats?.sales_data || []} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
              <defs>
                <linearGradient id="colorRevenue" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#818cf8" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#818cf8" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
              <XAxis dataKey="date" stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} />
              <YAxis stroke="#94a3b8" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(val) => `₹${val}`} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', borderRadius: '0.5rem', color: '#f1f5f9' }}
                itemStyle={{ color: '#818cf8' }}
              />
              <Area type="monotone" dataKey="revenue" stroke="#818cf8" strokeWidth={3} fillOpacity={1} fill="url(#colorRevenue)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2 rounded-xl border border-slate-800 bg-slate-900 p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-semibold text-slate-100">Recent Orders</h2>
            <Link to="/admin/orders" className="text-sm text-indigo-400 hover:text-indigo-300">View All</Link>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-slate-400">
              <thead className="text-xs uppercase bg-slate-800/50 text-slate-300">
                <tr>
                  <th className="px-4 py-3 rounded-l-lg">Order ID</th>
                  <th className="px-4 py-3">Customer</th>
                  <th className="px-4 py-3">Amount</th>
                  <th className="px-4 py-3">Status</th>
                  <th className="px-4 py-3 rounded-r-lg">Date</th>
                </tr>
              </thead>
              <tbody>
                {recentOrders.map((order) => (
                  <tr key={order.id} className="border-b border-slate-800/50 last:border-0 hover:bg-slate-800/20 transition-colors">
                    <td className="px-4 py-4 font-medium text-slate-200">#{order.id}</td>
                    <td className="px-4 py-4">{order.user?.first_name} {order.user?.last_name}</td>
                    <td className="px-4 py-4">{formatConvertedCurrency(order.total_price)}</td>
                    <td className="px-4 py-4">
                      <span className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-medium ${
                        order.status === 'delivered' ? 'bg-emerald-400/10 text-emerald-400' :
                        order.status === 'cancelled' ? 'bg-rose-500/10 text-rose-500' :
                        order.status === 'processing' ? 'bg-blue-400/10 text-blue-400' :
                        'bg-amber-400/10 text-amber-400'
                      }`}>
                        {order.status === 'delivered' ? <CheckCircle className="h-3.5 w-3.5" /> : 
                         order.status === 'cancelled' ? <XCircle className="h-3.5 w-3.5" /> :
                         order.status === 'processing' ? <Clock className="h-3.5 w-3.5" /> :
                         <Package className="h-3.5 w-3.5" />}
                        {order.status.charAt(0).toUpperCase() + order.status.slice(1)}
                      </span>
                    </td>
                    <td className="px-4 py-4">{new Date(order.created_at).toLocaleDateString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">
          <h2 className="text-lg font-semibold text-slate-100 mb-6">Quick Actions</h2>
          <div className="space-y-3">
            {[
              { label: "Add New Product", link: "/admin/products", icon: Package },
              { label: "View Analytics", link: "/admin/analytics", icon: TrendingUp },
              { label: "Manage Customers", link: "/admin/customers", icon: Users },
              { label: "Store Settings", link: "/admin/settings", icon: Settings },
            ].map((action, i) => (
              <Link key={i} to={action.link} className="flex items-center gap-3 rounded-lg border border-slate-800 bg-slate-800/30 p-4 transition-colors hover:bg-slate-800 hover:border-slate-700 group">
                <div className="rounded-lg bg-indigo-600/10 p-2 text-indigo-400 group-hover:bg-indigo-600 group-hover:text-white transition-colors">
                  <action.icon className="h-5 w-5" />
                </div>
                <span className="font-medium text-slate-200 group-hover:text-white">{action.label}</span>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
