import React from "react";
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
