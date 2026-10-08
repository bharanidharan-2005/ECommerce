import React from "react";
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
