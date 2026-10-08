import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Plus, Trash2, Tag, X, Percent, CheckCircle } from "lucide-react";
import { toast } from "react-hot-toast";
import api from "../../api/axios";
import { format } from "date-fns";

export default function AdminPromos() {
  const [promos, setPromos] = useState([]);
  const [loading, setLoading] = useState(true);
  
  // New promo form state
  const [showAddForm, setShowAddForm] = useState(false);
  const [newPromo, setNewPromo] = useState({
    code: "",
    discount_percentage: 10, min_order_amount: 0, valid_from: '', valid_until: '',
    active: true,
  });

  useEffect(() => {
    fetchPromos();
  }, []);

  const fetchPromos = async () => {
    try {
      const { data } = await api.get("/orders/admin-promos/");
      setPromos(data.results || data);
    } catch (err) {
      // It's possible the endpoint returns 404 if not implemented.
      // We will handle that gracefully.
      console.error(err);
      toast.error("Failed to load promo codes");
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    if (!newPromo.code) {
      toast.error("Promo code is required");
      return;
    }
    
    try {
      const payload = { ...newPromo };
      if (!payload.valid_from) delete payload.valid_from;
      if (!payload.valid_until) delete payload.valid_until;
      const { data } = await api.post("/orders/admin-promos/", payload);
      setPromos([data, ...promos]);
      setNewPromo({ code: "", discount_percentage: 10, min_order_amount: 0, valid_from: '', valid_until: '', active: true });
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
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
            <Tag className="h-6 w-6 text-indigo-400" /> 
            Promo Codes
          </h1>
          <p className="text-sm text-slate-400 mt-1">Manage discount codes and promotional campaigns</p>
        </div>
        <button
          onClick={() => setShowAddForm(!showAddForm)}
          className={`flex items-center gap-2 rounded-lg px-4 py-2 text-sm font-medium text-white transition-colors ${
            showAddForm 
              ? "bg-slate-700 hover:bg-slate-600" 
              : "bg-indigo-600 hover:bg-indigo-700"
          }`}
        >
          {showAddForm ? <X className="h-4 w-4" /> : <Plus className="h-4 w-4" />}
          {showAddForm ? "Cancel" : "Add Promo Code"}
        </button>
      </div>

      <AnimatePresence>
        {showAddForm && (
          <motion.form
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            className="bg-slate-900 p-6 rounded-xl border border-slate-800 shadow-xl"
            onSubmit={handleCreate}
          >
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-6">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Promo Code</label>
                <input
                  type="text"
                  required
                  className="w-full rounded-lg border border-slate-700 bg-slate-800/50 px-4 py-2.5 text-sm text-slate-200 uppercase placeholder-slate-500 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                  placeholder="e.g. SUMMER20"
                  value={newPromo.code}
                  onChange={(e) => setNewPromo({ ...newPromo, code: e.target.value.toUpperCase() })}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Discount Percentage</label>
                <div className="relative">
                  <Percent className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500" />
                  <input
                    type="number"
                    min="1"
                    max="100"
                    required
                    className="w-full rounded-lg border border-slate-700 bg-slate-800/50 pl-10 pr-4 py-2.5 text-sm text-slate-200 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                    value={newPromo.discount_percentage}
                    onChange={(e) => setNewPromo({ ...newPromo, discount_percentage: Number(e.target.value) })}
                  />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Min Order (₹)</label>
                <div className="relative">
                  <input
                    type="number"
                    min="0"
                    className="w-full rounded-lg border border-slate-700 bg-slate-800/50 px-4 py-2.5 text-sm text-slate-200 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                    value={newPromo.min_order_amount || 0}
                    onChange={(e) => setNewPromo({ ...newPromo, min_order_amount: Number(e.target.value) })}
                  />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Valid From</label>
                <input
                  type="datetime-local"
                  className="w-full rounded-lg border border-slate-700 bg-slate-800/50 px-4 py-2.5 text-sm text-slate-200 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                  value={newPromo.valid_from || ''}
                  onChange={(e) => setNewPromo({ ...newPromo, valid_from: e.target.value })}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">Valid Until</label>
                <input
                  type="datetime-local"
                  className="w-full rounded-lg border border-slate-700 bg-slate-800/50 px-4 py-2.5 text-sm text-slate-200 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                  value={newPromo.valid_until || ''}
                  onChange={(e) => setNewPromo({ ...newPromo, valid_until: e.target.value })}
                />
              </div>
              <div className="flex items-end">
                <button type="submit" className="w-full rounded-lg bg-emerald-600 px-4 py-2.5 text-sm font-medium text-white transition-colors hover:bg-emerald-700">
                  Create Code
                </button>
              </div>
            </div>
          </motion.form>
        )}
      </AnimatePresence>

      <div className="overflow-hidden rounded-xl border border-slate-800 bg-slate-900 shadow-xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="border-b border-slate-800 bg-slate-900/50 text-xs uppercase text-slate-300">
              <tr>
                <th className="py-4 pl-6 pr-3 font-semibold">Code</th>
                <th className="px-3 py-4 font-semibold">Discount</th>
                <th className="px-3 py-4 font-semibold">Status</th>
                <th className="px-3 py-4 font-semibold">Valid From</th>
                <th className="px-3 py-4 font-semibold">Valid Until</th>
                <th className="py-4 pr-6 pl-3 font-semibold text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {loading ? (
                <tr>
                  <td colSpan="6" className="py-12 text-center text-slate-400">
                    <div className="flex justify-center">
                      <div className="h-6 w-6 animate-spin rounded-full border-2 border-indigo-500 border-t-transparent"></div>
                    </div>
                  </td>
                </tr>
              ) : promos.length === 0 ? (
                <tr>
                  <td colSpan="6" className="py-12 text-center text-slate-400">
                    <div className="flex flex-col items-center justify-center">
                      <Tag className="h-12 w-12 text-slate-600 mb-3" />
                      <p>No promo codes found. Create your first one!</p>
                    </div>
                  </td>
                </tr>
              ) : (
                promos.map((promo) => (
                  <tr key={promo.id} className="hover:bg-slate-800/50 transition-colors">
                    <td className="py-4 pl-6 pr-3">
                      <span className="inline-flex items-center gap-1.5 rounded-md bg-indigo-500/10 px-2.5 py-1 text-sm font-mono font-medium text-indigo-400 border border-indigo-500/20">
                        {promo.code}
                      </span>
                    </td>
                    <td className="px-3 py-4 font-bold text-emerald-400">
                      {promo.discount_percentage}% OFF
                    </td>
                    <td className="px-3 py-4">
                      <button
                        onClick={() => handleToggleActive(promo)}
                        className={`inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-xs font-medium transition-colors ${
                          promo.active 
                            ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 hover:bg-emerald-500/20" 
                            : "bg-slate-700/50 text-slate-400 border border-slate-600 hover:bg-slate-700"
                        }`}
                      >
                        {promo.active ? (
                          <>
                            <CheckCircle className="h-3 w-3" /> Active
                          </>
                        ) : (
                          "Inactive"
                        )}
                      </button>
                    </td>
                    <td className="px-3 py-4 text-slate-400">
                      {promo.valid_from ? format(new Date(promo.valid_from), "MMM d, yyyy, h:mm a") : "-"}
                    </td>
                    <td className="px-3 py-4 text-slate-400">
                      {promo.valid_until ? format(new Date(promo.valid_until), "MMM d, yyyy, h:mm a") : "-"}
                    </td>
                    <td className="py-4 pr-6 pl-3 text-right">
                      <button
                        onClick={() => handleDelete(promo.id)}
                        className="text-slate-500 hover:text-rose-400 hover:bg-rose-400/10 p-2 rounded transition-colors"
                        title="Delete Code"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
