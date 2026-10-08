import os

components_dir = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\admin\settings\components"

files = {
    "OrderSettings.jsx": """import React from "react";
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
""",
    "CustomerSettings.jsx": """import React from "react";

export default function CustomerSettings() {
  return (
    <div className="space-y-8 animate-fade-in max-w-4xl">
      <div>
        <h2 className="text-xl font-semibold text-slate-100">Customer Settings</h2>
        <p className="text-sm text-slate-400 mt-1">Manage customer account rules and registration settings.</p>
      </div>

      <div className="space-y-6 bg-slate-900 border border-slate-800 rounded-lg p-6">
        <h3 className="text-lg font-medium text-slate-200 border-b border-slate-800 pb-3">Account Registration</h3>
        <div className="space-y-4">
          <label className="flex items-center gap-3 cursor-pointer">
            <input type="checkbox" defaultChecked className="w-5 h-5 rounded border-slate-700 bg-slate-800 text-indigo-600 focus:ring-indigo-500 focus:ring-offset-slate-900" />
            <div>
              <p className="text-slate-200 font-medium">Require Account for Checkout</p>
              <p className="text-slate-400 text-sm">Disable guest checkout.</p>
            </div>
          </label>
          <label className="flex items-center gap-3 cursor-pointer">
            <input type="checkbox" defaultChecked className="w-5 h-5 rounded border-slate-700 bg-slate-800 text-indigo-600 focus:ring-indigo-500 focus:ring-offset-slate-900" />
            <div>
              <p className="text-slate-200 font-medium">Email Verification</p>
              <p className="text-slate-400 text-sm">Require customers to verify email before ordering.</p>
            </div>
          </label>
        </div>
      </div>
    </div>
  );
}
""",
    "ShippingSettings.jsx": """import React from "react";
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
""",
    "PaymentSettings.jsx": """import React from "react";
import { CreditCard, Check, Monitor } from "lucide-react";

export default function PaymentSettings() {
  return (
    <div className="space-y-8 animate-fade-in max-w-4xl">
      <div>
        <h2 className="text-xl font-semibold text-slate-100">Payment Settings</h2>
        <p className="text-sm text-slate-400 mt-1">Manage payment gateways and methods available for customers.</p>
      </div>

      <div className="space-y-6 bg-slate-900 border border-slate-800 rounded-lg p-6">
        <h3 className="text-lg font-medium text-slate-200 border-b border-slate-800 pb-3">Active Providers</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-4 bg-slate-800/50 border border-slate-700/50 rounded-lg relative overflow-hidden">
            <div className="absolute top-0 right-0 bg-green-500/20 text-green-400 text-xs px-2 py-1 rounded-bl-lg font-medium">Active</div>
            <div className="flex items-center gap-3 mb-2">
              <CreditCard className="text-indigo-400 w-6 h-6" />
              <h4 className="text-slate-200 font-medium">Stripe Gateway</h4>
            </div>
            <p className="text-sm text-slate-400 mb-4">Accepts Credit/Debit Cards, Apple Pay, Google Pay.</p>
            <button className="text-indigo-400 text-sm font-medium hover:text-indigo-300">Configure</button>
          </div>
          
          <div className="p-4 bg-slate-800/50 border border-slate-700/50 rounded-lg relative overflow-hidden opacity-70">
            <div className="flex items-center gap-3 mb-2">
              <Monitor className="text-slate-400 w-6 h-6" />
              <h4 className="text-slate-300 font-medium">Razorpay (India)</h4>
            </div>
            <p className="text-sm text-slate-400 mb-4">Accepts UPI, Netbanking, Cards.</p>
            <button className="text-slate-300 text-sm font-medium hover:text-white bg-slate-700 px-3 py-1.5 rounded-lg">Connect</button>
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

print("Created Order, Customer, Shipping, and Payment Settings")
