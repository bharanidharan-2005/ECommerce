import React from 'react';
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
