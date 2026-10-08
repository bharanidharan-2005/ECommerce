import React, { useState } from "react";
import { 
  Globe, Lock, Bell, Store, ShoppingBag, Users, Truck, CreditCard, Calculator, RotateCcw, ShieldAlert, Activity, Save
} from "lucide-react";
import { useSettings } from "../../context/SettingsContext";

// Import all settings components
import GeneralSettings from "./settings/components/GeneralSettings";
import SecuritySettings from "./settings/components/SecuritySettings";
import NotificationSettings from "./settings/components/NotificationSettings";
import StoreSettings from "./settings/components/StoreSettings";
import OrderSettings from "./settings/components/OrderSettings";
import CustomerSettings from "./settings/components/CustomerSettings";
import ShippingSettings from "./settings/components/ShippingSettings";
import PaymentSettings from "./settings/components/PaymentSettings";
import TaxSettings from "./settings/components/TaxSettings";
import ReturnSettings from "./settings/components/ReturnSettings";
import AdminUsersSettings from "./settings/components/AdminUsersSettings";
import ActivityLogsSettings from "./settings/components/ActivityLogsSettings";

export default function AdminSettings() {
  const [activeTab, setActiveTab] = useState("general");
  const { loading, updateSettings } = useSettings();

  const tabs = [
    { id: "general", label: "General", icon: Globe, component: GeneralSettings },
    { id: "security", label: "Security", icon: Lock, component: SecuritySettings },
    { id: "notifications", label: "Notifications", icon: Bell, component: NotificationSettings },
    { id: "store", label: "Store", icon: Store, component: StoreSettings },
    { id: "orders", label: "Orders", icon: ShoppingBag, component: OrderSettings },
    { id: "customers", label: "Customers", icon: Users, component: CustomerSettings },
    { id: "shipping", label: "Shipping", icon: Truck, component: ShippingSettings },
    { id: "payments", label: "Payments", icon: CreditCard, component: PaymentSettings },
    { id: "tax", label: "Tax", icon: Calculator, component: TaxSettings },
    { id: "returns", label: "Returns & Refunds", icon: RotateCcw, component: ReturnSettings },
    { id: "users", label: "Admin Users", icon: ShieldAlert, component: AdminUsersSettings },
    { id: "logs", label: "Activity Logs", icon: Activity, component: ActivityLogsSettings },
  ];

  const handleSave = async () => {
    // We already update the context on change, but this simulates a master save button 
    // or we can just trigger a toast if we want. Context handles real save if needed.
    await updateSettings({});
  };

  const ActiveComponent = tabs.find(t => t.id === activeTab)?.component || GeneralSettings;

  return (
    <div className="space-y-6 w-full pb-20">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-2">
        <div>
          <h1 className="text-2xl font-bold text-slate-100">Settings</h1>
          <p className="text-sm text-slate-400 mt-1">Manage your ShopVerse store configuration.</p>
        </div>
        <button 
          onClick={handleSave} 
          disabled={loading}
          className={`flex items-center gap-2 rounded-lg bg-indigo-600 px-6 py-2.5 text-sm font-medium text-white transition-colors ${loading ? 'opacity-70 cursor-not-allowed' : 'hover:bg-indigo-700'}`}
        >
          <Save className="h-4 w-4" />
          {loading ? 'Saving...' : 'Save Settings'}
        </button>
      </div>

      <div className="flex flex-col lg:flex-row gap-6">
        {/* Mobile Dropdown */}
        <div className="lg:hidden">
          <select 
            value={activeTab}
            onChange={(e) => setActiveTab(e.target.value)}
            className="w-full rounded-lg border border-slate-700 bg-slate-900 px-4 py-3 text-slate-200 focus:border-indigo-500 focus:outline-none"
          >
            {tabs.map((tab) => (
              <option key={tab.id} value={tab.id}>{tab.label}</option>
            ))}
          </select>
        </div>

        {/* Desktop Sidebar */}
        <div className="hidden lg:block w-64 shrink-0 overflow-y-auto max-h-[calc(100vh-200px)] pr-2 custom-scrollbar">
          <nav className="flex flex-col space-y-1">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium transition-colors ${
                    activeTab === tab.id 
                      ? "bg-indigo-600/10 text-indigo-400 border border-indigo-500/20" 
                      : "text-slate-400 hover:bg-slate-800 hover:text-slate-200 border border-transparent"
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  {tab.label}
                </button>
              );
            })}
          </nav>
        </div>

        {/* Main Content Area */}
        <div className="flex-1 bg-slate-900/30 p-1 rounded-xl">
          <ActiveComponent />
        </div>
      </div>
    </div>
  );
}
