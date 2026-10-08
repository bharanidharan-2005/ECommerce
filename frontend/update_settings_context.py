import os

filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\context\SettingsContext.jsx"

content = """import React, { createContext, useContext, useState, useEffect } from 'react';
import toast from 'react-hot-toast';
import api from '../api/axios';

const SettingsContext = createContext(null);

export const useSettings = () => useContext(SettingsContext);

export const SettingsProvider = ({ children }) => {
  const [storeSettings, setStoreSettings] = useState({
    // General
    storeName: "ShopVerse",
    storeEmail: "contact@shopverse.com",
    supportEmail: "support@shopverse.com",
    phone: "+91 9876543210",
    description: "Premium E-commerce Store",
    storeStatus: "open",
    closureMessage: "We are temporarily closed.",
    currency: "INR",
    country: "India",
    timezone: "Asia/Kolkata",
    language: "English",
    dateFormat: "DD/MM/YYYY",
    numberFormat: "Indian",
    
    // Notifications
    emailNotifications: true,
    inAppNotifications: true,
    
    // Store (Business/Legal)
    legalBusinessName: "ShopVerse Technologies Pvt Ltd",
    gstin: "22AAAAA0000A1Z5",
    pan: "ABCDE1234F",
    businessAddress: "123 Tech Park",
    city: "Bangalore",
    state: "Karnataka",
    pinCode: "560001",
    
    // Order
    orderIdPrefix: "ORD",
    autoCancelUnpaid: true,
    cancelAfterHours: 24,
    
    // Shipping
    shippingEnabled: true,
    flatRate: 50,
    freeShippingThreshold: 500,
    
    // Tax
    taxEnabled: true,
    defaultTaxRate: 18,
    pricesIncludeTax: false,
    
    // Returns
    returnsEnabled: true,
    returnWindowDays: 7,
  });

  const [loading, setLoading] = useState(false);

  // Load from backend initially
  useEffect(() => {
    const fetchSettings = async () => {
      try {
        const res = await api.get('/auth/settings/');
        setStoreSettings(prev => ({ ...prev, ...res.data }));
      } catch (e) {
        console.error("Failed to fetch settings from backend", e);
        // Fallback to local storage if backend fails
        const saved = localStorage.getItem('shopverse_admin_settings');
        if (saved) {
          try {
            setStoreSettings(prev => ({ ...prev, ...JSON.parse(saved) }));
          } catch (err) {}
        }
      }
    };
    fetchSettings();
  }, []);

  const updateSettings = async (newSettings) => {
    setLoading(true);
    try {
      const updated = { ...storeSettings, ...newSettings };
      
      // Update backend
      await api.patch('/auth/settings/', updated);
      
      setStoreSettings(updated);
      localStorage.setItem('shopverse_admin_settings', JSON.stringify(updated));
      toast.success("Settings saved successfully");
      return true;
    } catch (err) {
      console.error("Failed to save settings", err);
      toast.error("Failed to save settings. Please try again.");
      return false;
    } finally {
      setLoading(false);
    }
  };

  return (
    <SettingsContext.Provider value={{ storeSettings, updateSettings, loading }}>
      {children}
    </SettingsContext.Provider>
  );
};
"""

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated SettingsContext.jsx to use real API calls")
