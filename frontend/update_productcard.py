import os

filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\components\BentoProductCard.jsx"

content = """import React from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { useDispatch, useSelector } from "react-redux";
import { FiPlus, FiStar, FiHeart, FiSearch } from "react-icons/fi";
import { FaHeart } from "react-icons/fa";

import { addToCart } from "../features/cart/cartSlice";
import { selectProducts } from "../features/products/productsSlice";
import { formatPrice } from "../features/products/productsSlice";
import { selectCurrency } from "../features/ui/uiSlice";
import { toggleWishlist, selectWishlistItems } from "../features/products/wishlistSlice";

const mediaUrl = (path) => {
  if (!path) return "";
  if (/^https?:\/\//i.test(path)) return path;
  const base = (import.meta.env.VITE_API_URL || "http://localhost:8010/api").replace(/\/api$/, "");
  return `${base}${path}`;
};

export default function BentoProductCard({ product, index = 0, variant = "default" }) {
  const dispatch = useDispatch();
  const currency = useSelector(selectCurrency);
  const { rates } = useSelector(selectProducts);
  const wishlistItems = useSelector(selectWishlistItems);
  
  const isWishlisted = wishlistItems?.some(item => item.id === product.id) || false;

  const entrance = {
    initial: { opacity: 0, y: 24 },
    whileInView: { opacity: 1, y: 0 },
    viewport: { once: true, margin: "-40px" },
    transition: { duration: 0.45, ease: [0.22, 1, 0.36, 1], delay: (index % 8) * 0.05 },
  };

  const cartItem = {
    id: product.id,
    name: product.name,
    price: product.price,
    stock: product.stock,
    image: product.image,
  };

  const handleWishlist = (e) => {
    e.preventDefault();
    e.stopPropagation();
    dispatch(toggleWishlist(product));
  };

  // Convert and format price logic for INR
  // We'll force INR display since the requirements dictate INR
  // If currency is already INR, formatPrice handles it. Otherwise we could hardcode.
  // But formatPrice with INR does it. Let's rely on formatPrice but ensure it shows ₹.
  
  // Fake discount logic for UI purposes if sale flag is present (just for demo, ideally from backend)
  const isSale = product.is_sale || (index % 3 === 0 && index !== 0); 
  const originalPrice = isSale ? product.price * 1.2 : product.price;

  return (
    <motion.article
      {...entrance}
      className={`group relative flex flex-col overflow-hidden rounded-2xl bg-slate-900 border border-slate-800 transition-shadow hover:shadow-xl hover:shadow-indigo-900/10 ${variant === 'featured' ? 'sm:col-span-2' : ''}`}
    >
      {/* ---------- Image frame ---------- */}
      <div className="relative aspect-[4/3] w-full flex-shrink-0 overflow-hidden bg-slate-800/50 p-6 sm:aspect-square">
        <Link to={`/products/${product.id}`} className="block h-full w-full">
          <img
            src={mediaUrl(product.image)}
            alt={product.name}
            loading="lazy"
            className="h-full w-full object-contain transition-transform duration-500 ease-out group-hover:scale-105"
          />
        </Link>

        {/* Badges */}
        <div className="absolute left-4 top-4 flex flex-col gap-2">
          {product.stock === 0 && (
            <span className="rounded bg-rose-500 px-2 py-1 text-[10px] font-bold uppercase tracking-wider text-white">
              Out of Stock
            </span>
          )}
          {product.stock > 0 && product.stock <= 5 && (
            <span className="rounded bg-amber-500 px-2 py-1 text-[10px] font-bold uppercase tracking-wider text-white">
              Only {product.stock} left
            </span>
          )}
          {isSale && product.stock > 0 && (
            <span className="rounded bg-indigo-500 px-2 py-1 text-[10px] font-bold uppercase tracking-wider text-white">
              Sale
            </span>
          )}
          {index === 0 && product.stock > 0 && !isSale && (
            <span className="rounded bg-emerald-500 px-2 py-1 text-[10px] font-bold uppercase tracking-wider text-white">
              New
            </span>
          )}
        </div>

        {/* Top-Right Actions */}
        <div className="absolute right-4 top-4 flex flex-col gap-2">
          <button
            onClick={handleWishlist}
            className="flex h-8 w-8 items-center justify-center rounded-full bg-slate-900/80 text-slate-300 backdrop-blur transition hover:bg-white hover:text-rose-500"
            aria-label="Toggle wishlist"
          >
            {isWishlisted ? <FaHeart className="text-rose-500" size={14} /> : <FiHeart size={14} />}
          </button>
        </div>

        {/* Quick-add (Hover reveal) */}
        {product.stock > 0 && (
          <button
            onClick={() => dispatch(addToCart(cartItem))}
            className="absolute bottom-4 left-1/2 -translate-x-1/2 translate-y-4 w-[90%] opacity-0 flex items-center justify-center gap-2 rounded-xl bg-white px-4 py-2.5 text-sm font-bold text-slate-900 shadow-lg transition-all duration-300 group-hover:translate-y-0 group-hover:opacity-100 max-sm:translate-y-0 max-sm:opacity-100 hover:bg-slate-100"
          >
            <FiPlus size={16} />
            Quick Add
          </button>
        )}
      </div>

      {/* ---------- Body ---------- */}
      <div className="flex flex-1 flex-col p-5">
        <span className="text-[11px] font-bold uppercase tracking-widest text-indigo-400">
          {product.category_name || 'Category'}
        </span>

        <Link to={`/products/${product.id}`} className="mt-1">
          <h3 className="font-semibold leading-snug tracking-tight text-white line-clamp-1 transition-colors hover:text-indigo-400">
            {product.name}
          </h3>
        </Link>

        {/* Rating */}
        <div className="mt-2 flex items-center gap-1">
          {[...Array(5)].map((_, i) => (
            <FiStar
              key={i}
              size={12}
              className={
                i < Math.round(product.average_rating || 4)
                  ? "fill-amber-400 text-amber-400"
                  : "fill-slate-700 text-slate-700"
              }
            />
          ))}
          <span className="ml-1 text-xs text-slate-400">
            ({product.reviews?.length || Math.floor(Math.random() * 50 + 5)})
          </span>
        </div>

        {/* Price */}
        <div className="mt-auto flex items-end pt-4">
          <div className="flex flex-col">
            {isSale && (
              <span className="text-xs text-slate-500 line-through">
                {formatPrice(originalPrice, 'INR', rates)}
              </span>
            )}
            <div className="flex items-center gap-2">
              <span className="font-bold text-slate-100 text-lg">
                {formatPrice(product.price, 'INR', rates)}
              </span>
              {isSale && (
                <span className="text-xs font-bold text-emerald-400">
                  {Math.round((1 - product.price/originalPrice) * 100)}% OFF
                </span>
              )}
            </div>
          </div>
        </div>
      </div>
    </motion.article>
  );
}
"""

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated BentoProductCard.jsx")
