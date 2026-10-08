# -*- coding: utf-8 -*-
import sys
import re
sys.stdout.reconfigure(encoding='utf-8')

filepath = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\ProductDetailPage.jsx'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Add wishlist state
state_target = '''const { rates } = useSelector(selectProducts);'''
state_new = '''const { rates } = useSelector(selectProducts);
  const wishlistItems = useSelector(selectWishlistItems) || [];
  const isWishlisted = wishlistItems.some(
    (item) => String(item.product) === String(product?.id) || String(item.product?.id) === String(product?.id) || String(item.product_details?.id) === String(product?.id)
  );'''

content = content.replace(state_target, state_new)

# Update action buttons
buttons_target = '''{/* Qty selector + Add-to-cart CTA */}
            {inStock && (
              <motion.div {...riseIn(0.35)} className="mt-7 flex items-stretch gap-3">
                <div className="flex items-center rounded-2xl border border-slate-700 bg-slate-800 px-1">
                  <button
                    onClick={() => setQty(Math.max(1, qty - 1))}
                    className="px-3.5 py-2.5 font-bold text-slate-400 transition hover:text-indigo-400"
                    aria-label="Decrease quantity"
                  >
                    −
                  </button>
                  <span className="w-8 text-center text-sm font-extrabold">{qty}</span>
                  <button
                    onClick={() => setQty(Math.min(product.stock, qty + 1))}
                    className="px-3.5 py-2.5 font-bold text-slate-400 transition hover:text-indigo-400"
                    aria-label="Increase quantity"
                  >
                    +
                  </button>
                </div>
                <button
                  onClick={() =>
                    dispatch(
                      addToCart({
                        id: product.id,
                        name: product.name,
                        price: product.price,
                        stock: product.stock,
                        image: product.image,
                        qty,
                      })
                    )
                  }
                  disabled={product.stock === 0}
                  className="btn-primary flex-1 !py-3.5 !text-base"
                >
                  <FiShoppingBag size={17} />
                  Add to Cart · {formatPrice(product.price * qty, currency, rates)}
                </button>
              </motion.div>
            )}'''

buttons_new = '''{/* Qty selector + Add-to-cart CTA */}
            <motion.div {...riseIn(0.35)} className="mt-7 flex items-stretch gap-3">
              {inStock ? (
                <>
                  <div className="flex items-center rounded-2xl border border-slate-700 bg-slate-800 px-1">
                    <button
                      onClick={() => setQty(Math.max(1, qty - 1))}
                      className="px-3.5 py-2.5 font-bold text-slate-400 transition hover:text-indigo-400"
                      aria-label="Decrease quantity"
                    >
                      −
                    </button>
                    <span className="w-8 text-center text-sm font-extrabold">{qty}</span>
                    <button
                      onClick={() => setQty(Math.min(product.stock, qty + 1))}
                      className="px-3.5 py-2.5 font-bold text-slate-400 transition hover:text-indigo-400"
                      aria-label="Increase quantity"
                    >
                      +
                    </button>
                  </div>
                  <button
                    onClick={() =>
                      dispatch(
                        addToCart({
                          id: product.id,
                          name: product.name,
                          price: product.price,
                          stock: product.stock,
                          image: product.image,
                          qty,
                        })
                      )
                    }
                    className="btn-primary flex-1 !py-3.5 !text-base"
                  >
                    <FiShoppingBag size={17} />
                    Add to Cart · {formatPrice(product.price * qty, currency, rates)}
                  </button>
                </>
              ) : (
                <button disabled className="btn-primary flex-1 !py-3.5 !text-base !bg-slate-800 !text-slate-500 !cursor-not-allowed">
                  Out of Stock
                </button>
              )}
              <button
                onClick={() => dispatch(toggleWishlist(product.id))}
                className={lex w-14 items-center justify-center rounded-2xl border transition-all \}
                aria-label="Toggle Wishlist"
              >
                <FiHeart size={20} className={isWishlisted ? "fill-rose-500" : ""} />
              </button>
            </motion.div>'''

content = content.replace(buttons_target, buttons_new)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print('Patched PDP successfully.')
