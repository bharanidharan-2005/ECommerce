import os
import re

footer_path = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\components\Footer.jsx'
with open(footer_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the state variables
old_state = '''  const [email, setEmail] = useState("");
  const [status, setStatus] = useState(""); // 'idle', 'loading', 'success', 'error'
  const [message, setMessage] = useState("");'''

new_state = '''  const [email, setEmail] = useState("");
  const [status, setStatus] = useState(""); // 'idle', 'loading', 'success', 'error'
  const [message, setMessage] = useState("");
  const [couponCode, setCouponCode] = useState("");
  const [copied, setCopied] = useState(false);'''

content = content.replace(old_state, new_state)

# Replace handleSubscribe
old_handle = '''  const handleSubscribe = async (e) => {
    e.preventDefault();
    if (!email) return;

    setStatus("loading");
    try {
      const response = await api.post("/auth/newsletter/subscribe/", { email });
      setStatus("success");
      setMessage(response.data.message || "Successfully subscribed!");
      setEmail("");
    } catch (err) {
      setStatus("error");
      setMessage(err.response?.data?.message || err.response?.data?.error || "Failed to subscribe. Please try again.");
    }
  };'''

new_handle = '''  const handleSubscribe = async (e) => {
    e.preventDefault();
    if (!email) return;

    setStatus("loading");
    try {
      const response = await api.post("/auth/newsletter/subscribe/", { email });
      setStatus("success");
      setMessage(response.data.message || "Successfully subscribed!");
      setCouponCode(response.data.coupon || "");
      setEmail("");
    } catch (err) {
      setStatus("error");
      setMessage(err.response?.data?.detail || err.response?.data?.message || err.response?.data?.error || "Failed to subscribe. Please try again.");
    }
  };

  const handleCopyCode = () => {
    if (couponCode) {
      navigator.clipboard.writeText(couponCode);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };'''

content = content.replace(old_handle, new_handle)

# Replace the UI
old_ui_regex = r'<div className="space-y-4">\s*<h3 className="text-sm font-bold text-white uppercase tracking-wider">Join our newsletter</h3>.*?</div>\s*</div>'
new_ui = '''<div className="space-y-4">
              {status !== "success" ? (
                <>
                  <h3 className="text-lg font-bold text-white uppercase tracking-wider">GET 10% OFF YOUR FIRST ORDER</h3>
                  <p className="text-slate-400 text-sm mb-4">
                    Subscribe to ShopVerse and get 10% off your first purchase, plus early access to new arrivals and exclusive deals.
                  </p>
                  <form className="flex flex-col sm:flex-row max-w-md gap-2" onSubmit={handleSubscribe}>
                    <input 
                      type="email" 
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="Enter your email address" 
                      disabled={status === "loading"}
                      className="flex-1 rounded-xl bg-slate-900 border border-slate-800 px-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition disabled:opacity-50"
                    />
                    <button 
                      type="submit" 
                      disabled={status === "loading"}
                      className="rounded-xl bg-indigo-600 px-6 py-3 text-sm font-bold text-white hover:bg-indigo-500 transition flex items-center justify-center disabled:opacity-50 whitespace-nowrap"
                    >
                      {status === "loading" ? "Wait..." : "GET 10% OFF"}
                    </button>
                  </form>
                  <p className="text-xs text-slate-500 mt-2">No spam. Unsubscribe anytime.</p>
                  {status === "error" && (
                    <div className="flex items-center gap-2 text-rose-400 text-sm mt-3 bg-rose-500/10 p-3 rounded-lg border border-rose-500/20">
                      <FiAlertCircle className="flex-shrink-0" />
                      <span>{message}</span>
                    </div>
                  )}
                </>
              ) : (
                <div className="bg-slate-900/50 p-6 rounded-2xl border border-indigo-500/30">
                  <div className="flex items-center gap-2 text-emerald-400 font-bold mb-2">
                    <FiCheck size={20} />
                    <span>You're in!</span>
                  </div>
                  <p className="text-white text-sm mb-4">Your 10% discount is ready.</p>
                  
                  {couponCode && (
                    <>
                      <div className="bg-slate-950 border border-slate-800 rounded-xl p-4 flex flex-col items-center justify-center mb-6">
                        <span className="text-xl font-black text-indigo-400 tracking-widest">{couponCode}</span>
                        <span className="text-xs text-slate-400 mt-1 uppercase font-bold tracking-wider">10% OFF your first order</span>
                      </div>
                      <p className="text-xs text-slate-400 text-center mb-6">Minimum order ₹999 • Valid for 7 days</p>
                      
                      <div className="flex flex-col sm:flex-row gap-3">
                        <button 
                          onClick={handleCopyCode}
                          className="flex-1 rounded-xl bg-slate-800 px-4 py-3 text-sm font-bold text-white hover:bg-slate-700 transition flex items-center justify-center border border-slate-700"
                        >
                          {copied ? "✓ Code copied!" : "COPY CODE"}
                        </button>
                        <Link 
                          to="/products"
                          className="flex-1 rounded-xl bg-indigo-600 px-4 py-3 text-sm font-bold text-white hover:bg-indigo-500 transition flex items-center justify-center gap-2"
                        >
                          SHOP NOW <FiArrowRight />
                        </Link>
                      </div>
                    </>
                  )}
                </div>
              )}
            </div>
          </div>'''

content = re.sub(old_ui_regex, new_ui, content, flags=re.DOTALL)

with open(footer_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Footer patched.")