$file = "C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\ProfilePage.jsx"
$content = Get-Content $file -Raw

$inputClass = "w-full rounded-xl border border-slate-700 bg-slate-800/50 px-4 py-3 text-sm text-white placeholder-slate-500 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 transition-colors"
$disabledClass = "w-full rounded-xl border border-slate-700 bg-slate-800/30 px-4 py-3 text-sm text-slate-500 cursor-not-allowed"

$content = $content -replace 'className="input-field"', "className=`"$inputClass`""
$content = $content -replace 'className="input-field opacity-50 cursor-not-allowed"', "className=`"$disabledClass`""

Set-Content $file $content -Encoding utf8
