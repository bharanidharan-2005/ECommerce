import React from 'react';
import { Link } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { FiHeart, FiShoppingCart, FiStar } from 'react-icons/fi';
import { addToCart } from '../features/cart/cartSlice';
import { toggleWishlist } from '../features/products/wishlistSlice';
import { formatPrice } from '../features/products/productsSlice';

export default function BentoProductCard({ product }) {
  const dispatch = useDispatch();
  const wishlistItems = useSelector((state) => state.wishlist.items) || [];
  const currency = useSelector((state) => state.ui.currency) || "INR";
  
  // A wishlist item usually has 'product' or 'product_details' containing the actual product info
  const isWishlisted = wishlistItems.some(item => 
    String(item.product) === String(product.id) || 
    String(item.product?.id) === String(product.id) || 
    String(item.product_details?.id) === String(product.id)
  );

  const handleAddToCart = (e) => {
    e.preventDefault();
    e.stopPropagation();
    dispatch(addToCart({ ...product, quantity: 1 }));
  };

  const handleToggleWishlist = (e) => {
    e.preventDefault();
    e.stopPropagation();
    dispatch(toggleWishlist(product.id)); // Pass product.id here
  };

  return (
    <Link 
      to={`/products/${product.id}`}
      className="group relative flex flex-col overflow-hidden rounded-3xl bg-slate-800 transition-all duration-300 hover:-translate-y-1 hover:shadow-xl hover:shadow-indigo-500/10 border border-slate-700/50 hover:border-indigo-500/30 h-full"
    >
      {/* Image Container */}
      <div className="relative aspect-square overflow-hidden bg-slate-900/50">
        <img
          src={product.image || 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&q=80'}
          alt={product.name}
          className="h-full w-full object-cover transition-transform duration-700 group-hover:scale-110"
        />
        
        {/* Badges */}
        <div className="absolute left-4 top-4 flex flex-col gap-2">
          {product.discount_percentage > 0 && (
            <span className="rounded-full bg-rose-500/90 px-3 py-1 text-xs font-bold text-white backdrop-blur-md">
              -{product.discount_percentage}% OFF
            </span>
          )}
        </div>

        {/* Wishlist Button */}
        <button
          onClick={handleToggleWishlist}
          className={`absolute right-4 top-4 flex h-10 w-10 items-center justify-center rounded-full backdrop-blur-md transition-all duration-300 ${
            isWishlisted ? 'bg-rose-500 text-white shadow-lg shadow-rose-500/20' : 'bg-slate-900/60 text-slate-300 hover:bg-slate-900'
          }`}
          aria-label="Toggle wishlist"
        >
          <FiHeart className={isWishlisted ? 'fill-current' : ''} size={18} />
        </button>

        {/* Quick Add Button (Hover) */}
        <div className="absolute bottom-4 left-4 right-4 translate-y-12 opacity-0 transition-all duration-300 group-hover:translate-y-0 group-hover:opacity-100">
          <button
            onClick={handleAddToCart}
            disabled={product.stock === 0}
            className={`flex w-full items-center justify-center gap-2 rounded-xl py-3 font-bold text-sm shadow-lg backdrop-blur-md transition-colors ${
              product.stock === 0
                ? 'bg-slate-800 text-slate-400 cursor-not-allowed'
                : 'bg-indigo-600/90 text-white hover:bg-indigo-500'
            }`}
          >
            <FiShoppingCart size={18} />
            {product.stock === 0 ? 'Out of Stock' : 'Quick Add'}
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="flex flex-1 flex-col p-5">
        <div className="mb-2 flex items-center justify-between gap-2">
          {/* Removing unexplained category integer/ID if it exists, leaving space for rating */}
          <div className="flex items-center gap-1 text-xs font-bold text-amber-400">
            <FiStar className="fill-current" />
            <span>{product.average_rating ? product.average_rating.toFixed(1) : '5.0'} ({product.reviews?.length || 0})</span>
          </div>
        </div>
        
        <h3 className="mb-2 text-lg font-bold text-white line-clamp-1 group-hover:text-indigo-300 transition-colors">
          {product.name}
        </h3>
        
        <div className="mt-auto pt-4 flex items-center justify-between border-t border-slate-700/50">
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
            <span className={`text-xs font-bold mt-1 ${product.stock === 0 ? 'text-rose-400' : product.stock <= 5 ? 'text-amber-400' : 'text-emerald-400'}`}>
              {product.stock === 0 ? 'Out of Stock' : product.stock <= 5 ? `Only ${product.stock} left` : 'In Stock'}
            </span>
          </div>
          
          {/* Mobile Add to cart (visible only on small screens) */}
          <button
            onClick={handleAddToCart}
            disabled={product.stock === 0}
            className={`lg:hidden flex h-10 w-10 items-center justify-center rounded-full transition-colors ${
              product.stock === 0
                ? 'bg-slate-800 text-slate-500'
                : 'bg-indigo-600/20 text-indigo-400 hover:bg-indigo-600 hover:text-white'
            }`}
          >
            <FiShoppingCart size={18} />
          </button>
        </div>
      </div>
    </Link>
  );
}