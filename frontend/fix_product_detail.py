import sys

filepath = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\ProductDetailPage.jsx'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

lines[235] = '                className={`flex w-14 items-center justify-center rounded-2xl border transition-all ${isWishlisted ? \'border-rose-500/50 bg-rose-500/10 text-rose-500 hover:bg-rose-500/20\' : \'border-slate-700 bg-slate-800 text-slate-400 hover:border-slate-600 hover:text-slate-300\'}`}\n'

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('Fixed ProductDetailPage.jsx with script file')
