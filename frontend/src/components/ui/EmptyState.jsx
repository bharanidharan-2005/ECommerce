import React from 'react';
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
