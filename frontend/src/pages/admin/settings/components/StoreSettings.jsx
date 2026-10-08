import React from "react";
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
