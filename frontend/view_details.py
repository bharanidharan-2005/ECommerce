file_path = 'src/pages/admin/AdminOrders.jsx'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

import_str = """import { useState, useEffect } from "react";
import { FiChevronDown, FiChevronUp, FiMapPin, FiPackage, FiCreditCard } from "react-icons/fi";
import { motion, AnimatePresence } from "framer-motion";
import api from "../../api/axios";
import { format } from "date-fns";
"""

content = content.replace('import { useState, useEffect } from "react";\nimport api from "../../api/axios";\nimport { format } from "date-fns";', import_str)

vars_str = """export default function AdminOrders() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [expandedOrderId, setExpandedOrderId] = useState(null);
"""
content = content.replace('export default function AdminOrders() {\n  const [orders, setOrders] = useState([]);\n  const [loading, setLoading] = useState(true);', vars_str)

toggle_func = """  const toggleExpand = (id) => {
    setExpandedOrderId(expandedOrderId === id ? null : id);
  };
"""

content = content.replace('  if (loading) return <div className="text-center py-12 text-slate-400">Loading orders...</div>;', toggle_func + '\n  if (loading) return <div className="text-center py-12 text-slate-400">Loading orders...</div>;')

old_tbody = """          <tbody className="divide-y divide-slate-800">
            {orders.map((order) => (
              <tr key={order.id} className="hover:bg-slate-800/50">"""

new_tbody = """          <tbody className="divide-y divide-slate-800">
            {orders.map((order) => (
              <React.Fragment key={order.id}>
              <tr className="hover:bg-slate-800/50 cursor-pointer transition-colors" onClick={() => toggleExpand(order.id)}>"""

# wait, we need to import React if we use React.Fragment, or we can just import { Fragment } from "react" 
# Better yet, just replace React.Fragment with <></>! No, JSX fragment requires import in some setups but not in modern React. Let's just import Fragment.

import_str = """import React, { useState, useEffect } from "react";
import { FiChevronDown, FiChevronUp, FiMapPin, FiPackage, FiCreditCard } from "react-icons/fi";
import { motion, AnimatePresence } from "framer-motion";
import api from "../../api/axios";
import { format } from "date-fns";
"""
content = content.replace('import { useState, useEffect } from "react";\nimport { FiChevronDown, FiChevronUp, FiMapPin, FiPackage, FiCreditCard } from "react-icons/fi";\nimport { motion, AnimatePresence } from "framer-motion";\nimport api from "../../api/axios";\nimport { format } from "date-fns";', import_str)

new_tbody = """          <tbody className="divide-y divide-slate-800">
            {orders.map((order) => (
              <React.Fragment key={order.id}>
              <tr className="hover:bg-slate-800/50 cursor-pointer transition-colors" onClick={() => toggleExpand(order.id)}>"""

content = content.replace(old_tbody, new_tbody)


# add expand icon and expanded section
old_action = """                  <select
                    value={order.status.charAt(0).toUpperCase() + order.status.slice(1)}
                    onChange={(e) => handleStatusChange(order.id, e.target.value)}"""

new_action = """                  <div className="flex items-center gap-2" onClick={(e) => e.stopPropagation()}>
                    <select
                      value={order.status.charAt(0).toUpperCase() + order.status.slice(1)}
                      onChange={(e) => handleStatusChange(order.id, e.target.value)}"""

content = content.replace(old_action, new_action)

old_action_end = """                  </select>
                </td>
              </tr>
            ))}"""

new_action_end = """                    </select>
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
                                  <span className="font-semibold text-slate-300">${parseFloat(item.subtotal).toFixed(2)}</span>
                                </div>
                              ))}
                              <div className="pt-2 flex justify-between items-center text-sm">
                                <span className="font-bold text-slate-400">Total</span>
                                <span className="text-lg font-black text-indigo-400">${parseFloat(order.total_price).toFixed(2)}</span>
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
                                  <span className="text-emerald-400 font-medium">Paid on {format(new Date(order.paid_at || order.created_at), "MMM d, yyyy")}</span>
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
            ))}"""

content = content.replace(old_action_end, new_action_end)

# Also fix the value of select option so it works properly matching uppercase
old_select = """                    <select
                      value={order.status.charAt(0).toUpperCase() + order.status.slice(1)}
                      onChange={(e) => handleStatusChange(order.id, e.target.value)}
                      className="rounded-md border border-slate-700 bg-slate-800 px-2 py-1 text-sm text-slate-200 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                    >
                      <option value="pending">Pending</option>
                      <option value="paid">Paid</option>
                      <option value="shipped">Shipped</option>
                      <option value="delivered">Delivered</option>
                      <option value="cancelled">Cancelled</option>
                    </select>"""

new_select = """                    <select
                      value={order.status.toLowerCase()}
                      onChange={(e) => handleStatusChange(order.id, e.target.value)}
                      className="rounded-md border border-slate-700 bg-slate-800 px-2 py-1 text-sm text-slate-200 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                    >
                      <option value="pending">Pending</option>
                      <option value="paid">Paid</option>
                      <option value="shipped">Shipped</option>
                      <option value="delivered">Delivered</option>
                      <option value="cancelled">Cancelled</option>
                    </select>"""
content = content.replace(old_select, new_select)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Added detailed expandable view to Admin Orders.")
