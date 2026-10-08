import os

filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\admin\AdminCustomers.jsx"

content = """import React, { useState, useEffect } from "react";
import api from "../../api/axios";
import { Search, Mail, Phone, Calendar, UserX, CheckCircle, Filter, Users as UsersIcon } from "lucide-react";
import { formatConvertedCurrency } from "../../utils/currency";
import toast from "react-hot-toast";
import { format } from "date-fns";

export default function AdminCustomers() {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");

  useEffect(() => {
    const fetchCustomers = async () => {
      try {
        const res = await api.get("/auth/admin/customers/"); 
        setCustomers(res.data.results || res.data || []);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchCustomers();
  }, []);

  const filteredCustomers = customers.filter(customer => {
    const matchesSearch = (customer.first_name?.toLowerCase() || "").includes(searchQuery.toLowerCase()) || 
                          (customer.last_name?.toLowerCase() || "").includes(searchQuery.toLowerCase()) ||
                          (customer.email?.toLowerCase() || "").includes(searchQuery.toLowerCase());
    
    // Status filter - assuming status might be active/inactive or similar. 
    // If backend doesn't provide status exactly, we just ignore for now or simulate
    const cStatus = customer.status?.toLowerCase() || "active";
    const matchesStatus = statusFilter === "all" || cStatus === statusFilter.toLowerCase();
    
    return matchesSearch && matchesStatus;
  });

  if (loading && customers.length === 0) {
    return <div className="text-center py-12 text-slate-400">Loading customers...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <h1 className="text-2xl font-bold text-slate-100">Customers</h1>
        <div className="flex flex-col sm:flex-row items-center gap-3 w-full sm:w-auto">
          <div className="relative w-full sm:w-64">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500" />
            <input 
              type="text" 
              placeholder="Search customers..." 
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full rounded-lg border border-slate-700 bg-slate-800/50 pl-10 pr-4 py-2 text-sm text-slate-200 placeholder-slate-400 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
            />
          </div>
          <div className="relative w-full sm:w-auto flex items-center gap-2">
            <Filter className="text-slate-400 h-4 w-4" />
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="w-full sm:w-auto rounded-lg border border-slate-700 bg-slate-800/50 px-3 py-2 text-sm text-slate-200 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
            >
              <option value="all">All Status</option>
              <option value="active">Active</option>
              <option value="inactive">Inactive</option>
            </select>
          </div>
        </div>
      </div>

      <div className="overflow-hidden rounded-xl border border-slate-800 bg-slate-900 shadow-xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="border-b border-slate-800 bg-slate-900/50 text-xs uppercase text-slate-300">
              <tr>
                <th className="py-4 pl-6 pr-3 font-semibold">Customer</th>
                <th className="px-3 py-4 font-semibold">Contact</th>
                <th className="px-3 py-4 font-semibold">Orders</th>
                <th className="px-3 py-4 font-semibold">Total Spent</th>
                <th className="px-3 py-4 font-semibold">Joined Date</th>
                <th className="px-3 py-4 font-semibold">Status</th>
                <th className="py-4 pr-6 pl-3 font-semibold text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {filteredCustomers.length === 0 ? (
                <tr>
                  <td colSpan="7" className="py-12 text-center text-slate-400">
                    <div className="flex flex-col items-center justify-center">
                      <UsersIcon className="h-12 w-12 text-slate-600 mb-3" />
                      <p>No customers found.</p>
                    </div>
                  </td>
                </tr>
              ) : filteredCustomers.map((customer) => (
                <tr key={customer.id} className="hover:bg-slate-800/50 transition-colors">
                  <td className="py-4 pl-6 pr-3">
                    <div className="flex items-center gap-3">
                      <div className="h-10 w-10 rounded-full bg-indigo-600 flex items-center justify-center text-white font-bold">
                        {customer.first_name ? customer.first_name.charAt(0) : (customer.email ? customer.email.charAt(0).toUpperCase() : 'U')}
                      </div>
                      <div>
                        <div className="font-medium text-slate-200">{customer.first_name} {customer.last_name}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-3 py-4">
                    <div className="flex items-center gap-2 text-slate-300">
                      <Mail className="h-4 w-4 text-slate-500" />
                      {customer.email}
                    </div>
                    {customer.phone && (
                      <div className="flex items-center gap-2 text-slate-300 mt-1">
                        <Phone className="h-4 w-4 text-slate-500" />
                        {customer.phone}
                      </div>
                    )}
                  </td>
                  <td className="px-3 py-4 text-slate-300 font-medium">
                    {customer.orders_count || 0}
                  </td>
                  <td className="px-3 py-4 text-slate-300 font-medium">
                    {formatConvertedCurrency(customer.total_spent || 0)}
                  </td>
                  <td className="px-3 py-4 text-slate-400">
                    <div className="flex items-center gap-1.5">
                      <Calendar className="h-4 w-4 text-slate-500" />
                      {customer.date_joined ? format(new Date(customer.date_joined), "MMM d, yyyy") : "N/A"}
                    </div>
                  </td>
                  <td className="px-3 py-4">
                    <span className="inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                      <CheckCircle className="h-3 w-3" />
                      {customer.status || "Active"}
                    </span>
                  </td>
                  <td className="py-4 pr-6 pl-3 text-right">
                    <button className="text-slate-400 hover:text-indigo-400 transition-colors font-medium">
                      View Details
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
"""

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated AdminCustomers.jsx")
