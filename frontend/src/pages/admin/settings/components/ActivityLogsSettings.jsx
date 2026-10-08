import React from "react";
import { Clock } from "lucide-react";

export default function ActivityLogsSettings() {
  return (
    <div className="space-y-8 animate-fade-in max-w-4xl">
      <div>
        <h2 className="text-xl font-semibold text-slate-100">Activity Logs</h2>
        <p className="text-sm text-slate-400 mt-1">View recent admin actions across the system.</p>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-lg overflow-hidden">
        <div className="p-4 border-b border-slate-800">
          <input type="text" placeholder="Search logs..." className="w-full md:w-64 rounded-lg border border-slate-700 bg-slate-800 px-4 py-2 text-sm text-slate-200 focus:border-indigo-500 focus:outline-none" />
        </div>
        <div className="divide-y divide-slate-800">
          {[1, 2, 3].map((_, idx) => (
            <div key={idx} className="p-4 flex items-start gap-4">
              <div className="p-2 bg-slate-800 rounded-lg mt-1">
                <Clock className="w-4 h-4 text-slate-400" />
              </div>
              <div>
                <p className="text-slate-200 text-sm"><strong>Store Owner</strong> updated <span className="text-indigo-400">Store Settings</span></p>
                <p className="text-slate-500 text-xs mt-1">Today at 10:45 AM</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
