import os

file_path = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\ProfilePage.jsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

coupon_manager_code = """
// --- COUPON MANAGER COMPONENT ---
const CouponManager = () => {
  const [coupon, setCoupon] = useState("");
  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchCoupon = async () => {
      try {
        const { data } = await api.get("/accounts/profile/coupon/");
        if (data.coupon) {
          setCoupon(data.coupon);
        } else {
          setError("You don't have a custom promo code yet.");
        }
      } catch (err) {
        setError("You are not subscribed to the newsletter.");
      } finally {
        setLoading(false);
      }
    };
    fetchCoupon();
  }, []);

  const handleSave = async (e) => {
    e.preventDefault();
    try {
      const { data } = await api.put("/accounts/profile/coupon/", { coupon });
      setCoupon(data.coupon);
      setIsEditing(false);
      toast.success(data.message || "Promo code updated!");
    } catch (err) {
      toast.error(err.response?.data?.error || "Failed to update promo code");
    }
  };

  const inputClass = "w-full rounded-xl border border-slate-700 bg-slate-800/50 px-4 py-3 text-sm text-white placeholder-slate-500 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 transition-colors uppercase";

  if (loading) return <div className="animate-pulse bg-slate-800 h-24 rounded-xl"></div>;

  return (
    <div className="card p-6 h-full flex flex-col">
      <h2 className="text-lg font-black tracking-tight mb-4 flex items-center gap-2">
        <FiDollarSign className="text-indigo-500" /> My Promo Code
      </h2>
      
      {error ? (
        <div className="flex flex-col items-center justify-center flex-1 text-center text-slate-400 border border-dashed border-slate-700 rounded-xl p-4">
          <p className="text-sm">{error}</p>
        </div>
      ) : isEditing ? (
        <form onSubmit={handleSave} className="space-y-4">
          <input 
            value={coupon} 
            onChange={(e) => setCoupon(e.target.value.toUpperCase())} 
            placeholder="Enter Custom Code" 
            className={inputClass}
            maxLength={15}
            required 
          />
          <div className="flex gap-3">
            <button type="button" onClick={() => setIsEditing(false)} className="btn-outline w-full !py-2">Cancel</button>
            <button type="submit" className="btn-primary w-full !py-2">Save</button>
          </div>
        </form>
      ) : (
        <div className="bg-emerald-500/10 border border-emerald-500/20 rounded-xl p-4 text-center flex flex-col justify-center flex-1">
          <p className="text-xs text-emerald-400/80 font-bold uppercase tracking-wider mb-2">Share this code for 10% off</p>
          <div className="text-2xl font-black text-emerald-400 tracking-widest">{coupon}</div>
          <button onClick={() => setIsEditing(true)} className="mt-4 text-emerald-400 text-sm font-bold hover:text-emerald-300 transition-colors underline underline-offset-4 decoration-emerald-500/30">Change Code</button>
        </div>
      )}
    </div>
  );
};

// --- ACCOUNT TAB COMPONENT ---
"""

content = content.replace("// --- ACCOUNT TAB COMPONENT ---", coupon_manager_code)

# Change grid cols and insert CouponManager
content = content.replace(
    '<div className="grid grid-cols-1 lg:grid-cols-2 gap-6">',
    '<div className="grid grid-cols-1 lg:grid-cols-3 gap-6">'
)

notifications_block = """<div className="card p-6">
          <h2 className="text-lg font-black tracking-tight mb-4 flex items-center gap-2">
            <FiBell className="text-indigo-500" /> Notifications
          </h2>
          <div className="space-y-4">
            {['Order Updates', 'Promotional Emails', 'Deals & Offers'].map(n => (
              <div key={n} className="flex items-center justify-between">
                <span className="text-sm font-medium text-slate-300">{n}</span>
                <div className="w-10 h-5 bg-indigo-500 rounded-full relative cursor-pointer">
                  <div className="w-4 h-4 bg-white rounded-full absolute right-0.5 top-0.5 shadow-sm"></div>
                </div>
              </div>
            ))}
          </div>
        </div>"""

if "<CouponManager />" not in content:
    content = content.replace(notifications_block, notifications_block + "\n        <CouponManager />")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated ProfilePage.jsx with CouponManager")
