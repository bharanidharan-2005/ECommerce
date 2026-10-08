import os

file_path = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\ProfilePage.jsx"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add import
import_stmt = 'import { saveShippingAddress } from "../features/cart/cartSlice";\n'
if import_stmt not in content:
    content = content.replace(
        'import { updateUser } from "../features/auth/authSlice";',
        'import { updateUser } from "../features/auth/authSlice";\n' + import_stmt
    )

# Add AddressManager component right before AccountTab
address_manager_code = """
// --- ADDRESS MANAGER COMPONENT ---
const AddressManager = () => {
  const dispatch = useDispatch();
  const savedAddress = useSelector((s) => s.cart.shippingAddress);
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    full_name: "",
    address_line_1: "",
    address_line_2: "",
    city: "",
    state: "",
    postal_code: "",
    country: "US"
  });

  useEffect(() => {
    if (savedAddress) {
      setFormData(savedAddress);
    }
  }, [savedAddress]);

  const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSave = (e) => {
    e.preventDefault();
    dispatch(saveShippingAddress(formData));
    setIsEditing(false);
    toast.success("Address saved successfully!");
  };

  const inputClass = "w-full rounded-xl border border-slate-700 bg-slate-800/50 px-4 py-3 text-sm text-white placeholder-slate-500 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 transition-colors";

  if (isEditing) {
    return (
      <form onSubmit={handleSave} className="space-y-4">
        <input name="full_name" required value={formData.full_name} onChange={handleChange} placeholder="Full Name" className={inputClass} />
        <input name="address_line_1" required value={formData.address_line_1} onChange={handleChange} placeholder="Street Address" className={inputClass} />
        <input name="address_line_2" value={formData.address_line_2} onChange={handleChange} placeholder="Apt, Suite, Unit (optional)" className={inputClass} />
        <div className="grid grid-cols-2 gap-4">
          <input name="city" required value={formData.city} onChange={handleChange} placeholder="City" className={inputClass} />
          <input name="state" required value={formData.state} onChange={handleChange} placeholder="State / Province" className={inputClass} />
        </div>
        <div className="grid grid-cols-2 gap-4">
          <input name="postal_code" required value={formData.postal_code} onChange={handleChange} placeholder="Postal Code" className={inputClass} />
          <input name="country" required value={formData.country} onChange={handleChange} placeholder="Country" className={inputClass} />
        </div>
        <div className="flex gap-3 pt-2">
          <button type="button" onClick={() => setIsEditing(false)} className="btn-outline w-full !py-2">Cancel</button>
          <button type="submit" className="btn-primary w-full !py-2">Save Address</button>
        </div>
      </form>
    );
  }

  return (
    <>
      {!savedAddress ? (
        <div className="flex flex-col items-center justify-center py-6 text-center text-slate-400 border border-dashed border-slate-700 rounded-xl">
          <p className="text-sm">No saved addresses yet.</p>
          <button onClick={() => setIsEditing(true)} className="mt-3 text-indigo-400 text-sm font-bold hover:text-indigo-300 transition-colors">+ Add Address</button>
        </div>
      ) : (
        <div className="bg-slate-800/50 rounded-xl p-4 border border-slate-700 text-sm">
          <p className="font-bold text-white mb-1">{savedAddress.full_name}</p>
          <p className="text-slate-400">{savedAddress.address_line_1}</p>
          {savedAddress.address_line_2 && <p className="text-slate-400">{savedAddress.address_line_2}</p>}
          <p className="text-slate-400">{savedAddress.city}, {savedAddress.state} {savedAddress.postal_code}</p>
          <p className="text-slate-400">{savedAddress.country}</p>
          <button onClick={() => setIsEditing(true)} className="mt-4 text-indigo-400 font-bold hover:text-indigo-300 transition-colors">Edit Address</button>
        </div>
      )}
    </>
  );
};

// --- ACCOUNT TAB COMPONENT ---
"""

content = content.replace("// --- ACCOUNT TAB COMPONENT ---", address_manager_code)

old_address_html = """<div className="flex flex-col items-center justify-center py-6 text-center text-slate-400 border border-dashed border-slate-700 rounded-xl">
            <p className="text-sm">No saved addresses yet.</p>
            <button className="mt-3 text-indigo-400 text-sm font-bold hover:text-indigo-300 transition-colors">+ Add Address</button>
          </div>"""

new_address_html = "<AddressManager />"

content = content.replace(old_address_html, new_address_html)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated ProfilePage.jsx with AddressManager")
