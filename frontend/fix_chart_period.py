import os

filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\admin\AdminDashboard.jsx"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# Replace states and fetch to support period
old_state = """  const [stats, setStats] = useState(null);
  const [recentOrders, setRecentOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [statsRes, ordersRes] = await Promise.all([
          api.get("/orders/admin/stats/"),
          api.get("/orders/admin/?limit=5")
        ]);"""

new_state = """  const [stats, setStats] = useState(null);
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
        ]);"""
content = content.replace(old_state, new_state)

# Update the Select to use periodDays
old_select = """          <select className="rounded-lg border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-slate-200 focus:border-indigo-500 focus:outline-none">
            <option>Last 7 Days</option>
            <option>Last 30 Days</option>
            <option>This Year</option>
          </select>"""

new_select = """          <select 
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
          </select>"""
content = content.replace(old_select, new_select)

# Update the Chart Title
old_chart_title = '<h2 className="text-lg font-semibold text-slate-100 mb-6">Revenue Trend (Last 7 Days)</h2>'
new_chart_title = '<h2 className="text-lg font-semibold text-slate-100 mb-6">Revenue Trend ({periodLabel})</h2>'
content = content.replace(old_chart_title, new_chart_title)

# Don't show "Loading dashboard..." full screen on every period change so it's less jarring, but keep the initial one
old_loading = """  if (loading) {
    return <div className="text-slate-400 p-8">Loading dashboard...</div>;
  }"""
new_loading = """  if (loading && !stats) {
    return <div className="text-slate-400 p-8">Loading dashboard...</div>;
  }"""
content = content.replace(old_loading, new_loading)

# The hook dependency array
old_dep = "  }, []);"
new_dep = "  }, [periodDays]);"
content = content.replace(old_dep, new_dep)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
print("AdminDashboard.jsx updated to support 30 days and year")
