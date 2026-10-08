import os

filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\components\ui\EmptyState.jsx"

content = """import React from 'react';
import { FiInbox, FiSearch, FiShoppingCart, FiFolderMinus } from 'react-icons/fi';
import { Link } from 'react-router-dom';

const icons = {
  inbox: FiInbox,
  search: FiSearch,
  cart: FiShoppingCart,
  folder: FiFolderMinus
};

export default function EmptyState({ 
  icon = "folder", 
  title = "No data found", 
  message = "There's nothing here yet.",
  actionText = null,
  actionLink = null,
  actionOnClick = null
}) {
  const IconComponent = icons[icon] || FiFolderMinus;

  return (
    <div className="flex flex-col items-center justify-center p-12 text-center bg-slate-800/30 rounded-2xl border border-slate-700/50">
      <div className="flex h-16 w-16 items-center justify-center rounded-full bg-slate-800 text-slate-400 mb-4 shadow-inner">
        <IconComponent size={28} />
      </div>
      <h3 className="text-xl font-bold text-white mb-2">{title}</h3>
      <p className="text-slate-400 max-w-sm mb-6">{message}</p>
      
      {actionText && actionLink && (
        <Link to={actionLink} className="inline-flex items-center justify-center gap-2 rounded-full bg-indigo-600 px-6 py-2.5 text-sm font-bold text-white transition hover:bg-indigo-500 shadow-md">
          {actionText}
        </Link>
      )}
      
      {actionText && actionOnClick && !actionLink && (
        <button onClick={actionOnClick} className="inline-flex items-center justify-center gap-2 rounded-full bg-indigo-600 px-6 py-2.5 text-sm font-bold text-white transition hover:bg-indigo-500 shadow-md">
          {actionText}
        </button>
      )}
    </div>
  );
}
"""

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

filepath_err = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\components\ui\ErrorState.jsx"

content_err = """import React from 'react';
import { FiAlertCircle, FiRefreshCw } from 'react-icons/fi';

export default function ErrorState({ 
  title = "Something went wrong", 
  message = "We couldn't load this content due to an error.",
  onRetry = null 
}) {
  return (
    <div className="flex flex-col items-center justify-center p-12 text-center bg-rose-500/10 rounded-2xl border border-rose-500/20">
      <div className="flex h-16 w-16 items-center justify-center rounded-full bg-rose-500/20 text-rose-400 mb-4 shadow-inner">
        <FiAlertCircle size={28} />
      </div>
      <h3 className="text-xl font-bold text-white mb-2">{title}</h3>
      <p className="text-slate-400 max-w-sm mb-6">{message}</p>
      
      {onRetry && (
        <button 
          onClick={onRetry} 
          className="inline-flex items-center justify-center gap-2 rounded-full bg-rose-600 px-6 py-2.5 text-sm font-bold text-white transition hover:bg-rose-500 shadow-md"
        >
          <FiRefreshCw size={16} /> Try Again
        </button>
      )}
    </div>
  );
}
"""

with open(filepath_err, "w", encoding="utf-8") as f:
    f.write(content_err)

print("Created EmptyState and ErrorState components")
