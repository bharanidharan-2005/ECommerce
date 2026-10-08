import React, { useState, useEffect } from "react";
import { FiChevronDown, FiChevronUp, FiMapPin, FiPackage, FiCreditCard, FiSearch, FiFilter, FiCalendar } from "react-icons/fi";
import EmptyState from "../../components/ui/EmptyState";
import { motion, AnimatePresence } from "framer-motion";
import api from "../../api/axios";
import { format } from "date-fns";
import { formatConvertedCurrency } from "../../utils/currency";

export default function AdminOrders() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [expandedOrderId, setExpandedOrderId] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const res = await api.get("/orders/admin/");
        setOrders(res.data.results || res.data);
      } catch (err) {
        console.error("Cannot fetch orders", err);
      } finally {
        setLoading(false);
      }
    };
    fetchOrders();
  }, []);

  const handleStatusChange = async (orderId, newStatus) => {
    try {
      await api.patch("/orders/admin/" + orderId + "/", { status: newStatus });
      setOrders(orders.map(o => o.id === orderId ? { ...o, status: newStatus } : o));
    } catch (err) {
      console.error("Failed to update status", err);
    }
  };

  const toggleExpand = (id) => {
    setExpandedOrderId(expandedOrderId === id ? null : id);
  };

  const filteredOrders = orders.filter(order => {
    const matchesSearch = (order.full_name || order.email || "").toLowerCase().includes(searchQuery.toLowerCase()) || 
                          order.id.toString().includes(searchQuery);
    const matchesStatus = statusFilter === "all" || order.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  if (loading) return <div className="text-center py-12 text-slate-400">Loading orders...</div>;

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <h1 className="text-2xl font-bold text-slate-100">Orders</h1>
        
        <div className="flex flex-col sm:flex-row items-center gap-3 w-full sm:w-auto">
          <div className="relative w-full sm:w-64">
            <FiSearch className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input 
              type="text" 
              placeholder="Search orders or customers..." 
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full rounded-lg border border-slate-700 bg-slate-800/50 pl-10 pr-4 py-2 text-sm text-slate-200 placeholder-slate-400 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
            />
          </div>
          
          <div className="relative w-full sm:w-auto flex items-center gap-2">
            <FiFilter className="text-slate-400" />
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="w-full sm:w-auto rounded-lg border border-slate-700 bg-slate-800/50 px-3 py-2 text-sm text-slate-200 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
            >
              <option value="all">All Status</option>
              <option value="pending">Pending</option>
              <option value="processing">Processing</option>
              <option value="shipped">Shipped</option>
              <option value="delivered">Delivered</option>
              <option value="cancelled">Cancelled</option>
            </select>
          </div>
        </div>
      </div>

      <div className="overflow-hidden rounded-xl border border-slate-800 bg-slate-900/50">
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead className="border-b border-slate-800 bg-slate-900/50">
              <tr>
                <th className="py-4 pl-6 pr-3 text-sm font-semibold text-slate-400">Order ID</th>
                <th className="px-3 py-4 text-sm font-semibold text-slate-400">Customer</th>
                <th className="px-3 py-4 text-sm font-semibold text-slate-400">Date</th>
                <th className="px-3 py-4 text-sm font-semibold text-slate-400">Total</th>
                <th className="px-3 py-4 text-sm font-semibold text-slate-400">Status</th>
                <th className="py-4 pr-6 pl-3 text-sm font-semibold text-slate-400">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {filteredOrders.length === 0 ? (
                <tr>
                  <td colSpan="10" className="py-8">
                    <EmptyState 
                      icon={FiPackage} 
                      title="No orders found" 
                      message={searchQuery || statusFilter !== 'all' ? "Try adjusting your filters" : "You haven't received any orders yet."}
                      actionText={searchQuery || statusFilter !== 'all' ? "Clear Filters" : undefined}
                      onAction={() => { setSearchQuery(""); setStatusFilter("all"); }}
                    />
                  </td>
                </tr>
              ) : filteredOrders.map((order) => (
                <React.Fragment key={order.id}>
                <tr className="hover:bg-slate-800/50 cursor-pointer transition-colors" onClick={() => toggleExpand(order.id)}>
                  <td className="py-4 pl-6 pr-3 text-sm font-medium text-slate-200">
                    #{order.id}
                  </td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-slate-400">
                    {order.full_name || order.email}
                  </td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm text-slate-400 flex items-center gap-1.5">
                    <FiCalendar className="text-slate-500" />
                    {format(new Date(order.created_at), "MMM d, yyyy, h:mm a")}
                  </td>
                  <td className="whitespace-nowrap px-3 py-4 text-sm font-medium text-slate-300">
                    {formatConvertedCurrency(order.total_price)}
                  </td>
                  <td className="whitespace-nowrap px-3 py-4">
                    <span
                      className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${
                        ['delivered', 'paid'].includes(order.status)
                          ? "bg-emerald-500/10 text-emerald-400"
                          : ['shipped'].includes(order.status)
                            ? "bg-amber-500/10 text-amber-400"
                            : ['processing'].includes(order.status)
                              ? "bg-blue-500/10 text-blue-400"
                              : order.status === 'cancelled'
                                ? "bg-red-500/10 text-red-400"
                                : "bg-slate-500/10 text-slate-400"
                      }`}
                    >
                      {order.status.charAt(0).toUpperCase() + order.status.slice(1)}
                    </span>
                  </td>
                  <td className="py-4 pr-6 pl-3">
                    <div className="flex items-center gap-2" onClick={(e) => e.stopPropagation()}>
                      <select
                        value={order.status}
                        onChange={(e) => handleStatusChange(order.id, e.target.value)}
                        className="rounded-md border border-slate-700 bg-slate-800 px-2 py-1 text-sm text-slate-200 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                      >
                        <option value="pending">Pending</option>
                        <option value="processing">Processing</option>
                        <option value="paid">Paid</option>
                        <option value="shipped">Shipped</option>
                        <option value="delivered">Delivered</option>
                        <option value="cancelled">Cancelled</option>
                      </select>
                      <button 
                        onClick={(e) => { e.stopPropagation(); toggleExpand(order.id); }}
                        className="p-1 text-slate-400 hover:text-indigo-400 hover:bg-indigo-500/10 rounded transition-colors"
                      >
                        {expandedOrderId === order.id ? <FiChevronUp size={20} /> : <FiChevronDown size={20} />}
                      </button>
                    </div>
                  </td>
                </tr>
                <AnimatePresence>
                  {expandedOrderId === order.id && (
                    <tr>
                      <td colSpan="6" className="p-0 border-t-0">
                        <motion.div
                          initial={{ height: 0, opacity: 0 }}
                          animate={{ height: "auto", opacity: 1 }}
                          exit={{ height: 0, opacity: 0 }}
                          transition={{ duration: 0.3 }}
                          className="overflow-hidden bg-slate-900/30"
                        >
                          <div className="p-6 grid gap-6 lg:grid-cols-2">
                            
                            {/* Order Items */}
                            <div className="bg-slate-800/40 rounded-xl p-5 border border-slate-700/50">
                              <h3 className="text-sm font-bold text-slate-300 uppercase tracking-wider mb-4 flex items-center gap-2">
                                <FiPackage className="text-indigo-400" /> Order Items ({order.items?.length || 0})
                              </h3>
                              <div className="space-y-3">
                                {order.items?.map((item, idx) => (
                                  <div key={idx} className="flex justify-between items-center text-sm py-2 border-b border-slate-700/30 last:border-0">
                                    <div className="flex items-center gap-3">
                                      <div className="w-10 h-10 bg-slate-800 rounded overflow-hidden">
                                        {item.image && <img src={item.image.startsWith('http') ? item.image : `http://localhost:8010${item.image}`} alt={item.product_name} className="w-full h-full object-cover" />}
                                      </div>
                                      <div>
                                        <p className="font-medium text-slate-200">{item.product_name}</p>
                                        <p className="text-xs text-slate-500">Qty: {item.quantity}</p>
                                      </div>
                                    </div>
                                    <span className="font-semibold text-slate-300">{formatConvertedCurrency(item.subtotal)}</span>
                                  </div>
                                ))}
                                <div className="pt-2 flex justify-between items-center text-sm">
                                  <span className="font-bold text-slate-400">Total</span>
                                  <span className="text-lg font-black text-indigo-400">{formatConvertedCurrency(order.total_price)}</span>
                                </div>
                              </div>
                            </div>

                            {/* Order Details */}
                            <div className="space-y-4">
                              <div className="bg-slate-800/40 rounded-xl p-5 border border-slate-700/50">
                                <h3 className="text-sm font-bold text-slate-300 uppercase tracking-wider mb-3 flex items-center gap-2">
                                  <FiMapPin className="text-indigo-400" /> Shipping Information
                                </h3>
                                <p className="text-sm text-slate-300 font-medium">{order.full_name}</p>
                                <p className="text-sm text-slate-400 mt-1">{order.address_line_1}</p>
                                {order.address_line_2 && <p className="text-sm text-slate-400">{order.address_line_2}</p>}
                                <p className="text-sm text-slate-400">{order.city}, {order.state} {order.postal_code}</p>
                                <p className="text-sm text-slate-400">{order.country}</p>
                              </div>
                              
                              <div className="bg-slate-800/40 rounded-xl p-5 border border-slate-700/50">
                                <h3 className="text-sm font-bold text-slate-300 uppercase tracking-wider mb-3 flex items-center gap-2">
                                  <FiCreditCard className="text-indigo-400" /> Payment Info
                                </h3>
                                <p className="text-sm text-slate-300 flex items-center gap-2">
                                  <span className="text-slate-500">Method:</span> 
                                  <span className="font-medium capitalize">{order.payment_method?.replace('upi_', '') || 'Unknown'}</span>
                                </p>
                                <p className="text-sm text-slate-300 flex items-center gap-2 mt-1">
                                  <span className="text-slate-500">Payment Status:</span>
                                  {order.is_paid ? (
                                    <span className="text-emerald-400 font-medium">Paid on {format(new Date(order.paid_at || order.created_at), "MMM d, yyyy, h:mm a")}</span>
                                  ) : (
                                    <span className="text-amber-400 font-medium">Pending</span>
                                  )}
                                </p>
                              </div>
                            </div>

                          </div>
                        </motion.div>
                      </td>
                    </tr>
                  )}
                </AnimatePresence>
                </React.Fragment>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
