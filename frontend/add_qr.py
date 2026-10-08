import os
import re

filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\CheckoutPage.jsx"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Import
if "QRCodeSVG" not in content:
    content = content.replace('import { motion, AnimatePresence } from "framer-motion";', 
        'import { motion, AnimatePresence } from "framer-motion";\nimport { QRCodeSVG } from "qrcode.react";')

# 2. Add QR Code
old_block = """              <div className="grid grid-cols-2 gap-4">
                <div className="bg-slate-800/30 p-4 rounded-xl border border-slate-800">
                  <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Deliver To</h3>
                  <p className="text-sm text-slate-300">{address.full_name}<br/>{address.address_line_1}, {address.city}</p>
                </div>
                <div className="bg-slate-800/30 p-4 rounded-xl border border-slate-800">
                  <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Payment</h3>
                  <p className="text-sm text-slate-300">{PAYMENT_METHODS.find(m => m.id === method)?.label}</p>
                  {method.startsWith('upi') && <p className="text-xs text-slate-500">{upiId}</p>}
                </div>
              </div>"""

new_block = """              <div className="grid grid-cols-2 gap-4">
                <div className="bg-slate-800/30 p-4 rounded-xl border border-slate-800">
                  <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Deliver To</h3>
                  <p className="text-sm text-slate-300">{address.full_name}<br/>{address.address_line_1}, {address.city}</p>
                </div>
                <div className="bg-slate-800/30 p-4 rounded-xl border border-slate-800">
                  <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Payment</h3>
                  <p className="text-sm text-slate-300">{PAYMENT_METHODS.find(m => m.id === method)?.label}</p>
                  {method.startsWith('upi') && <p className="text-xs text-slate-500">{upiId}</p>}
                </div>
              </div>

              {method.startsWith('upi') && (
                <div className="bg-white p-6 rounded-xl border border-slate-800 flex flex-col items-center justify-center text-center mt-6 shadow-xl relative overflow-hidden">
                  <div className="absolute top-0 left-0 w-full h-1 bg-indigo-500"></div>
                  <h3 className="text-sm font-bold text-slate-800 mb-4">Scan to Pay via {method === 'upi_gpay' ? 'Google Pay' : 'Paytm'}</h3>
                  <div className="bg-white p-2 rounded-2xl border border-slate-200 shadow-sm inline-block">
                    <QRCodeSVG 
                      value={`upi://pay?pa=pay@shopverse&pn=ShopVerse&am=${discountedTotal}&cu=INR`}
                      size={180}
                      level={"H"}
                      includeMargin={true}
                      imageSettings={{
                        src: method === 'upi_gpay' ? 'https://upload.wikimedia.org/wikipedia/commons/f/f2/Google_Pay_Logo.svg' : 'https://upload.wikimedia.org/wikipedia/commons/c/cd/Paytm_logo.png',
                        height: 40,
                        width: 40,
                        excavate: true,
                      }}
                    />
                  </div>
                  <p className="text-xs font-medium text-slate-500 mt-4 px-8">Please scan this QR code with your UPI app. Click below after completing payment.</p>
                </div>
              )}"""

content = content.replace(old_block, new_block)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated CheckoutPage with QR Code")
