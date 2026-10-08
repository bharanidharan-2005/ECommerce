import React from "react";
import { useSettings } from "../../../../context/SettingsContext";
import { formatCurrency } from "../../../../utils/currency";

export default function ShippingSettings() {
  const { storeSettings, updateSettings } = useSettings();

  const handleChange = (e) => {
    const value = e.target.type === 'checkbox' ? e.target.checked : e.target.value;
    updateSettings({ [e.target.name]: value });
  };

  return (
    <div className="space-y-8 animate-fade-in max-w-4xl">
      <div>
        <h2 className="text-xl font-semibold text-slate-100">Shipping Settings</h2>
        <p className="text-sm text-slate-400 mt-1">Manage delivery zones, shipping methods, and thresholds.</p>
      </div>

      <div className="space-y-6 bg-slate-900 border border-slate-800 rounded-lg p-6">
        <h3 className="text-lg font-medium text-slate-200 border-b border-slate-800 pb-3">General Shipping</h3>
        <label className="flex items-center gap-3 cursor-pointer">
          <input type="checkbox" name="shippingEnabled" checked={storeSettings.shippingEnabled} onChange={handleChange} className="w-5 h-5 rounded border-slate-700 bg-slate-800 text-indigo-600 focus:ring-indigo-500 focus:ring-offset-slate-900" />
          <span className="text-slate-200 font-medium">Enable Shipping</span>
        </label>
        
        {storeSettings.shippingEnabled && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-4">
            <div className="space-y-2">
              <label className="text-sm font-medium text-slate-300">Flat Rate Delivery Charge</label>
              <div className="relative">
                <span className="absolute left-3 top-2.5 text-slate-400">{storeSettings.currency === 'USD' ? '$' : '₹'}</span>
                <input type="number" name="flatRate" value={storeSettings.flatRate} onChange={handleChange} className="w-full rounded-lg border border-slate-700 bg-slate-800 pl-8 pr-4 py-2.5 text-slate-200 focus:border-indigo-500 focus:outline-none" />
              </div>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium text-slate-300">Free Shipping Threshold</label>
              <div className="relative">
                <span className="absolute left-3 top-2.5 text-slate-400">{storeSettings.currency === 'USD' ? '$' : '₹'}</span>
                <input type="number" name="freeShippingThreshold" value={storeSettings.freeShippingThreshold} onChange={handleChange} className="w-full rounded-lg border border-slate-700 bg-slate-800 pl-8 pr-4 py-2.5 text-slate-200 focus:border-indigo-500 focus:outline-none" />
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="space-y-6 bg-slate-900 border border-slate-800 rounded-lg p-6">
        <h3 className="text-lg font-medium text-slate-200 border-b border-slate-800 pb-3">Delivery Zones & COD</h3>
        <div className="space-y-4">
          <label className="flex items-center gap-3 cursor-pointer">
            <input type="checkbox" defaultChecked className="w-5 h-5 rounded border-slate-700 bg-slate-800 text-indigo-600 focus:ring-indigo-500 focus:ring-offset-slate-900" />
            <div>
              <p className="text-slate-200 font-medium">Allow Cash on Delivery (COD)</p>
              <p className="text-slate-400 text-sm">Allow users to pay upon delivery.</p>
            </div>
          </label>
        </div>
      </div>
    </div>
  );
}
