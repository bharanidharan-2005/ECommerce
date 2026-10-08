import React from "react";
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
