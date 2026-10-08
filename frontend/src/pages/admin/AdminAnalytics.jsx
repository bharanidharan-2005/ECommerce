import React, { useState, useEffect } from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, AreaChart, Area, PieChart, Pie, Cell, Legend } from "recharts";
import { TrendingUp, Users, DollarSign, ShoppingBag, PieChart as PieChartIcon, Activity } from "lucide-react";
import api from "../../api/axios";
import { formatConvertedCurrency } from "../../utils/currency";
import toast from "react-hot-toast";

const COLORS = ['#818cf8', '#34d399', '#fbbf24', '#f87171', '#a78bfa', '#60a5fa'];

export default function AdminAnalytics() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [days, setDays] = useState(7);

  useEffect(() => {
    const fetchStats = async () => {
      setLoading(true);
      try {
        const res = await api.get(`/orders/admin/stats/?days=${days}`);
        
        // Convert the sales_data revenue to INR
        const convertedSalesData = res.data.sales_data?.map(item => ({
          ...item,
          name: item.date, // Map 'date' to 'name' for the charts
          revenue: parseFloat((item.revenue * 96.10).toFixed(2))
        })) || [];
        
        setStats({ 
          ...res.data, 
          sales_data_inr: convertedSalesData 
        });
      } catch (err) {
        toast.error("Failed to load analytics");
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, [days]);

  if (loading) {
    return <div className="text-center py-12 text-slate-400">Loading analytics...</div>;
  }

  const salesData = stats?.sales_data_inr || [];
  const statusData = stats?.status_data || [];

  // Mock Sales by Category data since backend doesn't provide it yet
  const categoryData = [
    { name: "Electronics", value: 45000 },
    { name: "Clothing", value: 30000 },
    { name: "Accessories", value: 15000 },
    { name: "Home & Garden", value: 20000 },
    { name: "Sports", value: 12000 }
  ];

  const totalRevenue = stats?.total_revenue ? stats.total_revenue * 96.10 : 0;
  const aov = stats?.total_orders > 0 ? (totalRevenue / stats.total_orders) : 0;

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between sm:items-center gap-4">
        <h1 className="text-2xl font-bold text-slate-100">Analytics Overview</h1>
        <div className="flex gap-2">
          <select 
            value={days}
            onChange={(e) => setDays(Number(e.target.value))}
            className="rounded-lg border border-slate-700 bg-slate-800/50 px-3 py-2 text-sm text-slate-200 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
          >
            <option value={7}>Last 7 Days</option>
            <option value={30}>Last 30 Days</option>
            <option value={365}>This Year</option>
          </select>
          <button onClick={() => {
            if (!salesData.length) {
              toast.error("No data to export");
              return;
            }
            const headers = ["Date", "Orders", "Revenue (INR)", "Paid", "Delivered", "Pending"];
            const csvContent = [
              headers.join(","),
              ...salesData.map(row => `${row.name},${row.orders},${row.revenue},${row.paid || 0},${row.delivered || 0},${row.pending || 0}`)
            ].join("\n");
            
            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement("a");
            const url = URL.createObjectURL(blob);
            link.setAttribute("href", url);
            link.setAttribute("download", `analytics_export_${days}_days.csv`);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            toast.success("Export successful!");
          }} className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-indigo-700">
            Export Data
          </button>
        </div>
      </div>

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {[
          { title: "Total Revenue", value: formatConvertedCurrency(totalRevenue / 96.10), trend: "+12.5%", icon: DollarSign, color: "text-emerald-400" },
          { title: "Total Orders", value: stats?.total_orders || 0, trend: "+8.4%", icon: ShoppingBag, color: "text-indigo-400" },
          { title: "Avg. Order Value", value: formatConvertedCurrency(aov / 96.10), trend: "+3.2%", icon: Activity, color: "text-rose-400" },
          { title: "Active Customers", value: stats?.total_users || 0, trend: "+5.2%", icon: Users, color: "text-blue-400" },
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

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">
          <h2 className="text-lg font-semibold text-slate-100 mb-6">Revenue Trend</h2>
          <div className="h-80 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={salesData}>
                <defs>
                  <linearGradient id="colorRevenue" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#818cf8" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#818cf8" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                <XAxis dataKey="name" stroke="#64748b" tick={{fill: '#64748b'}} />
                <YAxis stroke="#64748b" tick={{fill: '#64748b'}} tickFormatter={(value) => `₹${value >= 1000 ? (value/1000).toFixed(0) + 'k' : value}`} />
                <RechartsTooltip 
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', borderRadius: '12px' }}
                  itemStyle={{ color: '#e2e8f0' }}
                  formatter={(value) => [`₹${value}`, "Revenue"]}
                />
                <Area type="monotone" dataKey="revenue" stroke="#818cf8" fillOpacity={1} fill="url(#colorRevenue)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
        
        <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">
          <h2 className="text-lg font-semibold text-slate-100 mb-6">Orders Volume</h2>
          <div className="h-80 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={salesData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                <XAxis dataKey="name" stroke="#64748b" tick={{fill: '#64748b'}} />
                <YAxis stroke="#64748b" tick={{fill: '#64748b'}} />
                <RechartsTooltip 
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', borderRadius: '12px' }}
                  itemStyle={{ color: '#e2e8f0' }}
                  cursor={{fill: '#1e293b'}}
                  formatter={(value) => [value, "Orders"]}
                />
                <Bar dataKey="orders" fill="#34d399" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">
          <h2 className="text-lg font-semibold text-slate-100 mb-6">Sales by Category</h2>
          <div className="h-80 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={categoryData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  fill="#8884d8"
                  paddingAngle={5}
                  dataKey="value"
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                >
                  {categoryData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <RechartsTooltip 
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', borderRadius: '12px' }}
                  itemStyle={{ color: '#e2e8f0' }}
                  formatter={(value) => [`₹${value}`, "Sales"]}
                />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="rounded-xl border border-slate-800 bg-slate-900 p-6">
          <h2 className="text-lg font-semibold text-slate-100 mb-6">Order Status Distribution</h2>
          <div className="h-80 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={statusData.length > 0 ? statusData : [{name: "No Data", value: 1}]}
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                >
                  {(statusData.length > 0 ? statusData : [{name: "No Data", value: 1}]).map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <RechartsTooltip 
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', borderRadius: '12px' }}
                  itemStyle={{ color: '#e2e8f0' }}
                  formatter={(value) => [value, "Orders"]}
                />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
