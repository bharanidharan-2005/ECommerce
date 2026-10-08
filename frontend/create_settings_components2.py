import os

components_dir = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\admin\settings\components"

files = {
    "NotificationSettings.jsx": """import React from "react";
import { useSettings } from "../../../../context/SettingsContext";

export default function NotificationSettings() {
  const { storeSettings, updateSettings } = useSettings();

  const handleToggle = (name) => {
    updateSettings({ [name]: !storeSettings[name] });
  };

  return (
    <div className="space-y-8 animate-fade-in max-w-4xl">
      <div>
        <h2 className="text-xl font-semibold text-slate-100">Notification Settings</h2>
        <p className="text-sm text-slate-400 mt-1">Configure when and how you receive alerts.</p>
      </div>

      <div className="space-y-6 bg-slate-900 border border-slate-800 rounded-lg p-6">
        <h3 className="text-lg font-medium text-slate-200 border-b border-slate-800 pb-3">Notification Channels</h3>
        <div className="space-y-4">
          <label className="flex items-center gap-3 cursor-pointer">
            <input type="checkbox" className="w-5 h-5 rounded border-slate-700 bg-slate-800 text-indigo-600 focus:ring-indigo-500 focus:ring-offset-slate-900" 
              checked={storeSettings.emailNotifications} 
              onChange={() => handleToggle("emailNotifications")} 
            />
            <div>
              <p className="text-slate-200 font-medium">Email Notifications</p>
              <p className="text-slate-400 text-sm">Receive alerts via store email address.</p>
            </div>
          </label>
          <label className="flex items-center gap-3 cursor-pointer">
            <input type="checkbox" className="w-5 h-5 rounded border-slate-700 bg-slate-800 text-indigo-600 focus:ring-indigo-500 focus:ring-offset-slate-900" 
              checked={storeSettings.inAppNotifications} 
              onChange={() => handleToggle("inAppNotifications")} 
            />
            <div>
              <p className="text-slate-200 font-medium">In-App Notifications</p>
              <p className="text-slate-400 text-sm">Receive alerts inside the admin dashboard.</p>
            </div>
          </label>
        </div>
      </div>

      <div className="space-y-6 bg-slate-900 border border-slate-800 rounded-lg p-6">
        <h3 className="text-lg font-medium text-slate-200 border-b border-slate-800 pb-3">Notification Events</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-4">
            <h4 className="text-sm font-medium text-slate-300 uppercase tracking-wider">Orders</h4>
            {['New Order Placed', 'Order Cancellation', 'Return Request'].map(event => (
              <label key={event} className="flex items-center gap-3 cursor-pointer">
                <input type="checkbox" defaultChecked className="w-4 h-4 rounded border-slate-700 bg-slate-800 text-indigo-600 focus:ring-indigo-500 focus:ring-offset-slate-900" />
                <span className="text-slate-300 text-sm">{event}</span>
              </label>
            ))}
          </div>
          <div className="space-y-4">
            <h4 className="text-sm font-medium text-slate-300 uppercase tracking-wider">Inventory & Customers</h4>
            {['Low Stock Alert', 'Out of Stock', 'New Customer Registration'].map(event => (
              <label key={event} className="flex items-center gap-3 cursor-pointer">
                <input type="checkbox" defaultChecked className="w-4 h-4 rounded border-slate-700 bg-slate-800 text-indigo-600 focus:ring-indigo-500 focus:ring-offset-slate-900" />
                <span className="text-slate-300 text-sm">{event}</span>
              </label>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
""",
    "StoreSettings.jsx": """import React from "react";
import { useSettings } from "../../../../context/SettingsContext";

export default function StoreSettings() {
  const { storeSettings, updateSettings } = useSettings();

  const handleChange = (e) => {
    updateSettings({ [e.target.name]: e.target.value });
  };

  return (
    <div className="space-y-8 animate-fade-in max-w-4xl">
      <div>
        <h2 className="text-xl font-semibold text-slate-100">Store / Legal Settings</h2>
        <p className="text-sm text-slate-400 mt-1">Manage your business and tax IDs, address, and legal policies.</p>
      </div>

      <div className="space-y-6 bg-slate-900 border border-slate-800 rounded-lg p-6">
        <h3 className="text-lg font-medium text-slate-200 border-b border-slate-800 pb-3">Business Information</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-2 md:col-span-2">
            <label className="text-sm font-medium text-slate-300">Legal Business Name</label>
            <input type="text" name="legalBusinessName" value={storeSettings.legalBusinessName} onChange={handleChange} className="w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-2.5 text-slate-200 focus:border-indigo-500 focus:outline-none" />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-300">GSTIN / Tax ID</label>
            <input type="text" name="gstin" value={storeSettings.gstin} onChange={handleChange} className="w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-2.5 text-slate-200 focus:border-indigo-500 focus:outline-none" />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-300">PAN / Registration Number</label>
            <input type="text" name="pan" value={storeSettings.pan} onChange={handleChange} className="w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-2.5 text-slate-200 focus:border-indigo-500 focus:outline-none" />
          </div>
        </div>
      </div>

      <div className="space-y-6 bg-slate-900 border border-slate-800 rounded-lg p-6">
        <h3 className="text-lg font-medium text-slate-200 border-b border-slate-800 pb-3">Registered Business Address</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-2 md:col-span-2">
            <label className="text-sm font-medium text-slate-300">Street Address</label>
            <input type="text" name="businessAddress" value={storeSettings.businessAddress} onChange={handleChange} className="w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-2.5 text-slate-200 focus:border-indigo-500 focus:outline-none" />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-300">City</label>
            <input type="text" name="city" value={storeSettings.city} onChange={handleChange} className="w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-2.5 text-slate-200 focus:border-indigo-500 focus:outline-none" />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-300">State / Province</label>
            <input type="text" name="state" value={storeSettings.state} onChange={handleChange} className="w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-2.5 text-slate-200 focus:border-indigo-500 focus:outline-none" />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-300">PIN / Zip Code</label>
            <input type="text" name="pinCode" value={storeSettings.pinCode} onChange={handleChange} className="w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-2.5 text-slate-200 focus:border-indigo-500 focus:outline-none" />
          </div>
        </div>
      </div>
      
      <div className="space-y-6 bg-slate-900 border border-slate-800 rounded-lg p-6">
        <h3 className="text-lg font-medium text-slate-200 border-b border-slate-800 pb-3">Store Policies</h3>
        <p className="text-sm text-slate-400">Configure your Privacy Policy, Terms of Service, and Shipping Policy from the Content Management section.</p>
        <button className="rounded-lg border border-slate-700 bg-slate-800 px-4 py-2 text-sm font-medium text-slate-300 hover:bg-slate-700 transition-colors">Manage Policies</button>
      </div>
    </div>
  );
}
"""
}

for name, content in files.items():
    with open(os.path.join(components_dir, name), "w", encoding="utf-8") as f:
        f.write(content)

print("Created Notification and Store Settings")
