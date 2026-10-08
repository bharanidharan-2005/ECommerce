import React from "react";
import { useSettings } from "../../../../context/SettingsContext";

export default function OrderSettings() {
  const { storeSettings, updateSettings } = useSettings();

  const handleChange = (e) => {
    const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
    updateSettings({ [e.target.name]: value });
  };

  return (
    <div className="space-y-8 animate-fade-in max-w-4xl">
      <div>
        <h2 className="text-xl font-semibold text-slate-100">Order Settings</h2>
        <p className="text-sm text-slate-400 mt-1">Configure order processing, IDs, and automation rules.</p>
      </div>

      <div className="space-y-6 bg-slate-900 border border-slate-800 rounded-lg p-6">
        <h3 className="text-lg font-medium text-slate-200 border-b border-slate-800 pb-3">Order Processing</h3>
        <div className="space-y-4 max-w-md">
          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-300">Order ID Prefix</label>
            <input type="text" name="orderIdPrefix" value={storeSettings.orderIdPrefix} onChange={handleChange} className="w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-2.5 text-slate-200 focus:border-indigo-500 focus:outline-none" />
            <p className="text-xs text-slate-500 mt-1">e.g., ORD-1001</p>
          </div>
        </div>
      </div>

      <div className="space-y-6 bg-slate-900 border border-slate-800 rounded-lg p-6">
        <h3 className="text-lg font-medium text-slate-200 border-b border-slate-800 pb-3">Automation & Cancellation</h3>
        <div className="space-y-4">
          <label className="flex items-center gap-3 cursor-pointer">
            <input type="checkbox" name="autoCancelUnpaid" checked={storeSettings.autoCancelUnpaid} onChange={handleChange} className="w-5 h-5 rounded border-slate-700 bg-slate-800 text-indigo-600 focus:ring-indigo-500 focus:ring-offset-slate-900" />
            <div>
              <p className="text-slate-200 font-medium">Auto-Cancel Unpaid Orders</p>
              <p className="text-slate-400 text-sm">Automatically cancel orders that remain unpaid after a certain time.</p>
            </div>
          </label>
          
          {storeSettings.autoCancelUnpaid && (
            <div className="space-y-2 max-w-md pl-8">
              <label className="text-sm font-medium text-slate-300">Cancel After (Hours)</label>
              <input type="number" name="cancelAfterHours" value={storeSettings.cancelAfterHours} onChange={handleChange} className="w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-2.5 text-slate-200 focus:border-indigo-500 focus:outline-none" />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
