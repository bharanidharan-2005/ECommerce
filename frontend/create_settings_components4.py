import os

components_dir = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\admin\settings\components"

files = {
    "TaxSettings.jsx": """import React from "react";
import { useSettings } from "../../../../context/SettingsContext";

export default function TaxSettings() {
  const { storeSettings, updateSettings } = useSettings();

  const handleChange = (e) => {
    const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
    updateSettings({ [e.target.name]: value });
  };

  return (
    <div className="space-y-8 animate-fade-in max-w-4xl">
      <div>
        <h2 className="text-xl font-semibold text-slate-100">Tax Settings</h2>
        <p className="text-sm text-slate-400 mt-1">Configure global tax calculation and display options.</p>
      </div>

      <div className="space-y-6 bg-slate-900 border border-slate-800 rounded-lg p-6">
        <h3 className="text-lg font-medium text-slate-200 border-b border-slate-800 pb-3">Calculation</h3>
        <div className="space-y-4">
          <label className="flex items-center gap-3 cursor-pointer">
            <input type="checkbox" name="taxEnabled" checked={storeSettings.taxEnabled} onChange={handleChange} className="w-5 h-5 rounded border-slate-700 bg-slate-800 text-indigo-600 focus:ring-indigo-500 focus:ring-offset-slate-900" />
            <div>
              <p className="text-slate-200 font-medium">Enable Taxes</p>
              <p className="text-slate-400 text-sm">Calculate taxes on checkout.</p>
            </div>
          </label>
          <label className="flex items-center gap-3 cursor-pointer">
            <input type="checkbox" name="pricesIncludeTax" checked={storeSettings.pricesIncludeTax} onChange={handleChange} className="w-5 h-5 rounded border-slate-700 bg-slate-800 text-indigo-600 focus:ring-indigo-500 focus:ring-offset-slate-900" />
            <div>
              <p className="text-slate-200 font-medium">Prices include tax</p>
              <p className="text-slate-400 text-sm">Product prices in the catalog already include tax.</p>
            </div>
          </label>
          
          {storeSettings.taxEnabled && (
            <div className="space-y-2 max-w-md pt-2">
              <label className="text-sm font-medium text-slate-300">Default Tax Rate (%)</label>
              <input type="number" name="defaultTaxRate" value={storeSettings.defaultTaxRate} onChange={handleChange} className="w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-2.5 text-slate-200 focus:border-indigo-500 focus:outline-none" />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
""",
    "ReturnSettings.jsx": """import React from "react";
import { useSettings } from "../../../../context/SettingsContext";

export default function ReturnSettings() {
  const { storeSettings, updateSettings } = useSettings();

  const handleChange = (e) => {
    const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
    updateSettings({ [e.target.name]: value });
  };

  return (
    <div className="space-y-8 animate-fade-in max-w-4xl">
      <div>
        <h2 className="text-xl font-semibold text-slate-100">Returns & Refunds</h2>
        <p className="text-sm text-slate-400 mt-1">Configure your return policy rules and conditions.</p>
      </div>

      <div className="space-y-6 bg-slate-900 border border-slate-800 rounded-lg p-6">
        <h3 className="text-lg font-medium text-slate-200 border-b border-slate-800 pb-3">Return Rules</h3>
        <div className="space-y-4 max-w-md">
          <label className="flex items-center gap-3 cursor-pointer mb-4">
            <input type="checkbox" name="returnsEnabled" checked={storeSettings.returnsEnabled} onChange={handleChange} className="w-5 h-5 rounded border-slate-700 bg-slate-800 text-indigo-600 focus:ring-indigo-500 focus:ring-offset-slate-900" />
            <span className="text-slate-200 font-medium">Enable Returns</span>
          </label>
          
          {storeSettings.returnsEnabled && (
            <div className="space-y-2">
              <label className="text-sm font-medium text-slate-300">Return Window (Days)</label>
              <input type="number" name="returnWindowDays" value={storeSettings.returnWindowDays} onChange={handleChange} className="w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-2.5 text-slate-200 focus:border-indigo-500 focus:outline-none" />
              <p className="text-xs text-slate-500 mt-1">Number of days after delivery a customer can request a return.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
""",
    "AdminUsersSettings.jsx": """import React from "react";

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
""",
    "ActivityLogsSettings.jsx": """import React from "react";
import { Clock } from "lucide-react";

export default function ActivityLogsSettings() {
  return (
    <div className="space-y-8 animate-fade-in max-w-4xl">
      <div>
        <h2 className="text-xl font-semibold text-slate-100">Activity Logs</h2>
        <p className="text-sm text-slate-400 mt-1">View recent admin actions across the system.</p>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-lg overflow-hidden">
        <div className="p-4 border-b border-slate-800">
          <input type="text" placeholder="Search logs..." className="w-full md:w-64 rounded-lg border border-slate-700 bg-slate-800 px-4 py-2 text-sm text-slate-200 focus:border-indigo-500 focus:outline-none" />
        </div>
        <div className="divide-y divide-slate-800">
          {[1, 2, 3].map((_, idx) => (
            <div key={idx} className="p-4 flex items-start gap-4">
              <div className="p-2 bg-slate-800 rounded-lg mt-1">
                <Clock className="w-4 h-4 text-slate-400" />
              </div>
              <div>
                <p className="text-slate-200 text-sm"><strong>Store Owner</strong> updated <span className="text-indigo-400">Store Settings</span></p>
                <p className="text-slate-500 text-xs mt-1">Today at 10:45 AM</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
"""
}

for name, content in files.items():
    with open(os.path.join(components_dir, name), "w", encoding="utf-8") as f:
        f.write(content)

print("Created Tax, Return, AdminUsers, ActivityLogs Settings")
