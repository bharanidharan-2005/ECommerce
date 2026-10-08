import os

components_dir = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\admin\settings\components"

files = {
    "GeneralSettings.jsx": """import React from "react";
import { useSettings } from "../../../../context/SettingsContext";

export default function GeneralSettings() {
  const { storeSettings, updateSettings } = useSettings();

  const handleChange = (e) => {
    updateSettings({ [e.target.name]: e.target.value });
  };

  return (
    <div className="space-y-8 animate-fade-in max-w-4xl">
      <div>
        <h2 className="text-xl font-semibold text-slate-100">General Settings</h2>
        <p className="text-sm text-slate-400 mt-1">Manage your basic store information and regional settings.</p>
      </div>

      <div className="space-y-6 bg-slate-900 border border-slate-800 rounded-lg p-6">
        <h3 className="text-lg font-medium text-slate-200 border-b border-slate-800 pb-3">Store Information</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-300">Store Name</label>
            <input type="text" name="storeName" value={storeSettings.storeName} onChange={handleChange} className="w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-2.5 text-slate-200 focus:border-indigo-500 focus:outline-none" />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-300">Store Email</label>
            <input type="email" name="storeEmail" value={storeSettings.storeEmail} onChange={handleChange} className="w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-2.5 text-slate-200 focus:border-indigo-500 focus:outline-none" />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-300">Support Email</label>
            <input type="email" name="supportEmail" value={storeSettings.supportEmail} onChange={handleChange} className="w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-2.5 text-slate-200 focus:border-indigo-500 focus:outline-none" />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-300">Phone</label>
            <input type="text" name="phone" value={storeSettings.phone} onChange={handleChange} className="w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-2.5 text-slate-200 focus:border-indigo-500 focus:outline-none" />
          </div>
          <div className="space-y-2 md:col-span-2">
            <label className="text-sm font-medium text-slate-300">Store Description</label>
            <textarea name="description" value={storeSettings.description} onChange={handleChange} rows="3" className="w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-2.5 text-slate-200 focus:border-indigo-500 focus:outline-none" />
          </div>
        </div>
      </div>

      <div className="space-y-6 bg-slate-900 border border-slate-800 rounded-lg p-6">
        <h3 className="text-lg font-medium text-slate-200 border-b border-slate-800 pb-3">Store Status</h3>
        <div className="space-y-4">
          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-300">Status</label>
            <select name="storeStatus" value={storeSettings.storeStatus} onChange={handleChange} className="w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-2.5 text-slate-200 focus:border-indigo-500 focus:outline-none">
              <option value="open">Open</option>
              <option value="maintenance">Maintenance</option>
              <option value="closed">Closed</option>
            </select>
          </div>
          {storeSettings.storeStatus !== 'open' && (
            <div className="space-y-2">
              <label className="text-sm font-medium text-slate-300">Closure/Maintenance Message</label>
              <textarea name="closureMessage" value={storeSettings.closureMessage} onChange={handleChange} rows="2" className="w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-2.5 text-slate-200 focus:border-indigo-500 focus:outline-none" />
            </div>
          )}
        </div>
      </div>

      <div className="space-y-6 bg-slate-900 border border-slate-800 rounded-lg p-6">
        <h3 className="text-lg font-medium text-slate-200 border-b border-slate-800 pb-3">Regional Settings</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-300">Currency</label>
            <select name="currency" value={storeSettings.currency} onChange={handleChange} className="w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-2.5 text-slate-200 focus:border-indigo-500 focus:outline-none">
              <option value="INR">INR (?)</option>
              <option value="USD">USD ($)</option>
              <option value="EUR">EUR (€)</option>
              <option value="GBP">GBP (£)</option>
            </select>
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-300">Country</label>
            <input type="text" name="country" value={storeSettings.country} onChange={handleChange} className="w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-2.5 text-slate-200 focus:border-indigo-500 focus:outline-none" />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-300">Timezone</label>
            <select name="timezone" value={storeSettings.timezone} onChange={handleChange} className="w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-2.5 text-slate-200 focus:border-indigo-500 focus:outline-none">
              <option value="Asia/Kolkata">Asia/Kolkata (IST)</option>
              <option value="America/New_York">America/New_York (EST)</option>
              <option value="Europe/London">Europe/London (GMT)</option>
            </select>
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-300">System Language</label>
            <select name="language" value={storeSettings.language} onChange={handleChange} className="w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-2.5 text-slate-200 focus:border-indigo-500 focus:outline-none">
              <option value="English">English</option>
              <option value="Hindi">Hindi</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  );
}
""",
    "SecuritySettings.jsx": """import React from "react";
import { Shield, Key, Smartphone, Monitor } from "lucide-react";

export default function SecuritySettings() {
  return (
    <div className="space-y-8 animate-fade-in max-w-4xl">
      <div>
        <h2 className="text-xl font-semibold text-slate-100">Security Settings</h2>
        <p className="text-sm text-slate-400 mt-1">Manage admin account security, authentication, and active sessions.</p>
      </div>

      <div className="space-y-6 bg-slate-900 border border-slate-800 rounded-lg p-6">
        <div className="flex items-center gap-3 border-b border-slate-800 pb-3">
          <Key className="w-5 h-5 text-indigo-400" />
          <h3 className="text-lg font-medium text-slate-200">Admin Account Password</h3>
        </div>
        <div className="space-y-4 max-w-md">
          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-300">Current Password</label>
            <input type="password" placeholder="••••••••" className="w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-2.5 text-slate-200 focus:border-indigo-500 focus:outline-none" />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-300">New Password</label>
            <input type="password" placeholder="••••••••" className="w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-2.5 text-slate-200 focus:border-indigo-500 focus:outline-none" />
          </div>
          <button className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700 transition-colors">Update Password</button>
        </div>
      </div>

      <div className="space-y-6 bg-slate-900 border border-slate-800 rounded-lg p-6">
        <div className="flex items-center gap-3 border-b border-slate-800 pb-3">
          <Smartphone className="w-5 h-5 text-indigo-400" />
          <h3 className="text-lg font-medium text-slate-200">Two-Factor Authentication (2FA)</h3>
        </div>
        <div className="flex items-center justify-between p-4 bg-slate-800/50 border border-slate-700/50 rounded-lg">
          <div>
            <h4 className="text-slate-200 font-medium">Authenticator App</h4>
            <p className="text-slate-400 text-sm mt-1">Use an app like Google Authenticator to protect your account.</p>
          </div>
          <button className="rounded-lg bg-slate-700 px-4 py-2 text-sm font-medium text-white hover:bg-slate-600 transition-colors">Enable</button>
        </div>
      </div>

      <div className="space-y-6 bg-slate-900 border border-slate-800 rounded-lg p-6">
        <div className="flex items-center gap-3 border-b border-slate-800 pb-3">
          <Monitor className="w-5 h-5 text-indigo-400" />
          <h3 className="text-lg font-medium text-slate-200">Active Sessions</h3>
        </div>
        <div className="space-y-3">
          <div className="flex items-center justify-between p-4 bg-slate-800/50 border border-slate-700/50 rounded-lg">
            <div className="flex items-start gap-4">
              <Monitor className="w-8 h-8 text-slate-400 p-1.5 bg-slate-700 rounded-md" />
              <div>
                <h4 className="text-slate-200 font-medium">Windows • Chrome</h4>
                <p className="text-slate-400 text-sm mt-1">192.168.1.10 • Current Session</p>
              </div>
            </div>
          </div>
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

print("Created General and Security Settings")
