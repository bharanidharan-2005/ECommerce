import React from "react";

export default function AdminUsersSettings() {
  return (
    <div className="space-y-8 animate-fade-in max-w-4xl">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-xl font-semibold text-slate-100">Admin Users & Roles</h2>
          <p className="text-sm text-slate-400 mt-1">Manage staff accounts and their access permissions.</p>
        </div>
        <button className="bg-indigo-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-700 transition-colors">Add User</button>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-lg overflow-hidden">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-slate-800 bg-slate-900/50">
              <th className="px-6 py-4 text-sm font-medium text-slate-400">User</th>
              <th className="px-6 py-4 text-sm font-medium text-slate-400">Role</th>
              <th className="px-6 py-4 text-sm font-medium text-slate-400">Status</th>
              <th className="px-6 py-4 text-sm font-medium text-slate-400">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800">
            <tr>
              <td className="px-6 py-4">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-full bg-indigo-500 flex items-center justify-center text-white font-bold text-xs">SV</div>
                  <div>
                    <p className="text-slate-200 font-medium">Store Owner</p>
                    <p className="text-slate-500 text-xs">admin@shopverse.com</p>
                  </div>
                </div>
              </td>
              <td className="px-6 py-4 text-slate-300 text-sm">Super Admin</td>
              <td className="px-6 py-4"><span className="inline-block px-2.5 py-1 bg-green-500/20 text-green-400 rounded-full text-xs font-medium">Active</span></td>
              <td className="px-6 py-4 text-indigo-400 text-sm cursor-pointer hover:text-indigo-300">Edit</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
