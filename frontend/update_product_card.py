import sys

filepath = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\components\BentoProductCard.jsx'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Badges replacement
target_badges = '''        {/* Badges */}
        <div className="absolute left-4 top-4 flex flex-col gap-2">
          {product.stock <= 5 && product.stock > 0 && (
            <span className="rounded-full bg-rose-500/90 px-3 py-1 text-xs font-bold text-white backdrop-blur-md">
              Low Stock
            </span>
          )}
          {product.is_new && (
            <span className="rounded-full bg-indigo-500/90 px-3 py-1 text-xs font-bold text-white backdrop-blur-md">
              New
            </span>
          )}
        </div>'''

replacement_badges = '''        {/* Badges */}
        <div className="absolute left-4 top-4 flex flex-col gap-2">
          {product.discount_percentage > 0 && (
            <span className="rounded-full bg-rose-500/90 px-3 py-1 text-xs font-bold text-white backdrop-blur-md">
              -{product.discount_percentage}% OFF
            </span>
          )}
        </div>'''
content = content.replace(target_badges, replacement_badges)


# Category / Rating replacement
target_cat_rating = '''        <div className="mb-2 flex items-center justify-between gap-2">
          <span className="text-xs font-bold tracking-wider text-indigo-400 uppercase truncate">
            {product.category}
          </span>
          <div className="flex items-center gap-1 text-xs font-bold text-amber-400">
            <FiStar className="fill-current" />
            <span>4.8</span>
          </div>
        </div>'''

replacement_cat_rating = '''        <div className="mb-2 flex items-center justify-between gap-2">
          {/* Removing unexplained category integer/ID if it exists, leaving space for rating */}
          <div className="flex items-center gap-1 text-xs font-bold text-amber-400">
            <FiStar className="fill-current" />
            <span>{product.average_rating ? product.average_rating.toFixed(1) : '5.0'} ({product.reviews?.length || 0})</span>
          </div>
        </div>'''
content = content.replace(target_cat_rating, replacement_cat_rating)


# Price / Savings replacement
target_price = '''        <div className="mt-auto pt-4 flex items-center justify-between border-t border-slate-700/50">
          <div className="flex flex-col">
            <span className="text-lg font-black text-white">
              {formatPrice(product.price, currency)}
            </span>
          </div>'''

replacement_price = '''        <div className="mt-auto pt-4 flex items-center justify-between border-t border-slate-700/50">
          <div className="flex flex-col gap-1">
            <div className="flex items-baseline gap-2">
              <span className="text-lg font-black text-white">
                {formatPrice(product.price, currency)}
              </span>
              {product.original_price && product.original_price > product.price && (
                <span className="text-xs text-slate-400 line-through">
                  {formatPrice(product.original_price, currency)}
                </span>
              )}
            </div>
            {product.original_price && product.original_price > product.price && (
              <span className="text-xs font-bold text-emerald-400">
                Save {formatPrice(product.original_price - product.price, currency)}
              </span>
            )}
            
            {/* Stock State */}
            <span className={	ext-xs font-bold mt-1 }>
              {product.stock === 0 ? 'Out of Stock' : product.stock <= 5 ? Only  left : 'In Stock'}
            </span>
          </div>'''
content = content.replace(target_price, replacement_price)


with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated BentoProductCard.jsx')
