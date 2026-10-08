import os

filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\admin\AdminPromos.jsx"

content = """import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { FiPlus, FiTrash2, FiEdit2, FiCheck, FiX, FiTag } from "react-icons/fi";
import { toast } from "react-hot-toast";
import api from "../../services/api";

export default function AdminPromos() {
  const [promos, setPromos] = useState([]);
  const [loading, setLoading] = useState(true);
  
  // New promo form state
  const [showAddForm, setShowAddForm] = useState(false);
  const [newPromo, setNewPromo] = useState({
    code: "",
    discount_percentage: 10,
    active: true,
  });

  useEffect(() => {
    fetchPromos();
  }, []);

  const fetchPromos = async () => {
    try {
      const { data } = await api.get("/orders/admin-promos/");
      setPromos(data);
    } catch (err) {
      toast.error("Failed to load promo codes");
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      const { data } = await api.post("/orders/admin-promos/", newPromo);
      setPromos([data, ...promos]);
      setNewPromo({ code: "", discount_percentage: 10, active: true });
      setShowAddForm(false);
      toast.success("Promo code created!");
    } catch (err) {
      toast.error("Error creating promo code");
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this promo code?")) return;
    try {
      await api.delete(`/orders/admin-promos/${id}/`);
      setPromos(promos.filter((p) => p.id !== id));
      toast.success("Deleted promo code");
    } catch (err) {
      toast.error("Failed to delete");
    }
  };

  const handleToggleActive = async (promo) => {
    try {
      const { data } = await api.patch(`/orders/admin-promos/${promo.id}/`, {
        active: !promo.active
      });
      setPromos(promos.map((p) => (p.id === promo.id ? data : p)));
      toast.success(data.active ? "Promo activated" : "Promo deactivated");
    } catch (err) {
      toast.error("Update failed");
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
            <FiTag /> Promo Codes
          </h1>
          <p className="text-sm text-slate-400 mt-1">Manage discount codes and promotions</p>
        </div>
        <button
          onClick={() => setShowAddForm(!showAddForm)}
          className="btn-primary flex items-center gap-2"
        >
          {showAddForm ? <FiX /> : <FiPlus />}
          {showAddForm ? "Cancel" : "Add Promo"}
        </button>
      </div>

      {showAddForm && (
        <motion.form
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: "auto" }}
          className="bg-slate-800 p-6 rounded-xl border border-slate-700"
          onSubmit={handleCreate}
        >
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Code</label>
              <input
                type="text"
                required
                className="input uppercase"
                placeholder="e.g. SUMMER20"
                value={newPromo.code}
                onChange={(e) => setNewPromo({ ...newPromo, code: e.target.value.toUpperCase() })}
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Discount %</label>
              <input
                type="number"
                min="1"
                max="100"
                required
                className="input"
                value={newPromo.discount_percentage}
                onChange={(e) => setNewPromo({ ...newPromo, discount_percentage: Number(e.target.value) })}
              />
            </div>
            <div className="flex items-end">
              <button type="submit" className="btn-primary w-full h-[42px]">
                Create Code
              </button>
            </div>
          </div>
        </motion.form>
      )}

      {loading ? (
        <div className="text-center text-slate-400 py-10 animate-pulse">Loading promos...</div>
      ) : (
        <div className="bg-slate-800 rounded-xl border border-slate-700 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left">
              <thead>
                <tr className="bg-slate-900/50 text-slate-400 text-xs uppercase tracking-wider">
                  <th className="p-4">Code</th>
                  <th className="p-4">Discount</th>
                  <th className="p-4">Status</th>
                  <th className="p-4">Created</th>
                  <th className="p-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-700">
                {promos.length === 0 ? (
                  <tr>
                    <td colSpan="5" className="p-8 text-center text-slate-500">
                      No promo codes found. Create one above!
                    </td>
                  </tr>
                ) : (
                  promos.map((promo) => (
                    <tr key={promo.id} className="hover:bg-slate-750 transition-colors">
                      <td className="p-4">
                        <span className="font-mono font-bold text-indigo-400 bg-indigo-400/10 px-2 py-1 rounded">
                          {promo.code}
                        </span>
                      </td>
                      <td className="p-4 font-bold text-emerald-400">{promo.discount_percentage}% OFF</td>
                      <td className="p-4">
                        <button
                          onClick={() => handleToggleActive(promo)}
                          className={`px-3 py-1 rounded-full text-xs font-bold ${
                            promo.active ? "bg-emerald-500/20 text-emerald-400" : "bg-slate-600 text-slate-300"
                          }`}
                        >
                          {promo.active ? "Active" : "Inactive"}
                        </button>
                      </td>
                      <td className="p-4 text-slate-400 text-sm">
                        {new Date(promo.created_at).toLocaleDateString()}
                      </td>
                      <td className="p-4 text-right">
                        <button
                          onClick={() => handleDelete(promo.id)}
                          className="text-red-400 hover:bg-red-400/10 p-2 rounded transition-colors"
                          title="Delete Code"
                        >
                          <FiTrash2 />
                        </button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
"""

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
print("Created AdminPromos.jsx")
