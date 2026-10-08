import React from "react";
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
