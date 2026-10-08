/**
 * ProductDetailPage — immersive PDP matching the Bento design system.
 *
 *  - Left: large rounded media frame with slow scale-on-hover zoom
 *  - Right: sticky purchase panel (price, rating, stock, qty, CTA)
 *  - Below: customer reviews as floating white cards
 *  - Framer Motion staggers each section's entrance; skeleton mirrors layout
 */
import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { motion } from "framer-motion";
import { FiArrowLeft, FiCheck, FiShoppingBag, FiStar, FiTruck, FiHeart, FiMessageSquare } from "react-icons/fi";
import { toast } from "react-toastify";

import api from "../api/axios";


import PageTransition from "../components/PageTransition.jsx";
import { addToCart } from "../features/cart/cartSlice";
import { fetchProduct } from "../features/products/productsSlice";
import { selectProducts, formatPrice } from "../features/products/productsSlice";
import { selectCurrency } from "../features/ui/uiSlice";
import { toggleWishlist, selectWishlistItems } from "../features/products/wishlistSlice";

/** Passes absolute API image URLs straight through; resolves relative ones */
const mediaUrl = (path) => {
  if (!path) return "";
  if (/^https?:\/\//i.test(path) || path.startsWith('data:image')) return path;
  const base = (import.meta.env.VITE_API_URL || "http://localhost:8010/api").replace(/\/api$/, "");
  return `${base}${path}`;
};

/** Shared entrance animation for staggered sections */
const riseIn = (delay = 0) => ({
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.45, delay, ease: [0.22, 1, 0.36, 1] },
});

export default function ProductDetailPage() {
  const { id } = useParams();
  const dispatch = useDispatch();
  const { current: product, detailLoading } = useSelector((s) => s.products);
  const { user } = useSelector((s) => s.auth);
  const [qty, setQty] = useState(1);
  const currency = useSelector(selectCurrency);
  const { rates } = useSelector(selectProducts);
  const wishlistItems = useSelector(selectWishlistItems) || [];
  const isWishlisted = wishlistItems.some(
    (item) => String(item.product) === String(product?.id) || String(item.product?.id) === String(product?.id) || String(item.product_details?.id) === String(product?.id)
  );
  
  const [rating, setRating] = useState(5);
  const [comment, setComment] = useState("");
  const [reviewLoading, setReviewLoading] = useState(false);

  const submitReview = async (e) => {
    e.preventDefault();
    if (!comment.trim()) return toast.error("Please enter a comment");
    setReviewLoading(true);
    try {
      await api.post(`/products/${id}/reviews/`, { rating, comment });
      toast.success("Review submitted!");
      setComment("");
      setRating(5);
      dispatch(fetchProduct(id));
    } catch (err) {
      toast.error(err.response?.data?.non_field_errors?.[0] || "Failed to submit review");
    } finally {
      setReviewLoading(false);
    }
  };


  /* Refetch whenever the route param changes; scroll to top like a fresh page */
  useEffect(() => {
    dispatch(fetchProduct(id));
    window.scrollTo(0, 0);
  }, [dispatch, id]);

  /* ---------- Loading skeleton (mirrors final layout) ---------- */
  if (detailLoading || !product) {
    return (
      <div className="mx-auto max-w-7xl px-4 pt-32 pb-10 sm:px-6">
        <div className="grid gap-10 lg:grid-cols-2">
          <div className="skeleton aspect-square w-full !rounded-3xl" />
          <div className="flex flex-col gap-4 py-4">
            <div className="skeleton h-3 w-24" />
            <div className="skeleton h-8 w-3/4" />
            <div className="skeleton h-4 w-40" />
            <div className="skeleton h-9 w-32" />
            <div className="skeleton h-20 w-full" />
            <div className="skeleton h-12 w-full !rounded-2xl" />
          </div>
        </div>
      </div>
    );
  }

  const inStock = product.stock > 0;

  return (
    <PageTransition>
      <div className="mx-auto max-w-7xl px-4 pt-32 pb-8 sm:px-6">
        {/* Breadcrumb / back link */}
        <Link
          to="/products"
          className="mb-6 inline-flex items-center gap-1.5 text-sm font-semibold text-slate-400 transition hover:text-indigo-400"
        >
          <FiArrowLeft size={15} /> Back to collection
        </Link>

        <div className="grid gap-10 lg:grid-cols-2 lg:gap-14">
          {/* ================= Media frame ================= */}
          <motion.div {...riseIn(0)} className="group relative overflow-hidden rounded-3xl shadow-float">
            <img
              src={mediaUrl(product.image)}
              alt={product.name}
              className="aspect-square w-full object-cover transition-transform duration-700 ease-out group-hover:scale-105"
            />
            {/* Low-stock ribbon */}
            {inStock && product.stock <= 5 && (
              <span className="absolute left-5 top-5 rounded-full bg-amber-500/95 px-3.5 py-1.5 text-xs font-bold text-white shadow-md">
                Only {product.stock} left
              </span>
            )}
          </motion.div>

          {/* ================= Purchase panel (sticky on desktop) ================= */}
          <div className="lg:sticky lg:top-24 lg:self-start">
            <motion.span
              {...riseIn(0.05)}
              className="text-xs font-bold uppercase tracking-widest text-indigo-400"
            >
              {product.category_name}
            </motion.span>

            <motion.h1
              {...riseIn(0.1)}
              className="mt-2 text-3xl font-black leading-tight tracking-tight sm:text-4xl"
            >
              {product.name}
            </motion.h1>

            {/* Rating */}
            <motion.div {...riseIn(0.15)} className="mt-3 flex items-center gap-1.5">
              <div className="flex gap-0.5">
                {[...Array(5)].map((_, i) => (
                  <FiStar
                    key={i}
                    size={16}
                    className={
                      i < Math.round(product.average_rating)
                        ? "fill-amber-400 text-amber-400"
                        : "fill-slate-700 text-slate-700"
                    }
                  />
                ))}
              </div>
              <span className="text-sm font-medium text-slate-400">
                {product.average_rating} · {product.reviews?.length ?? 0} reviews
              </span>
            </motion.div>

            {/* Price */}
            <motion.p {...riseIn(0.2)} className="mt-4 text-4xl font-black tracking-tight">
              {formatPrice(product.price, currency, rates)}
            </motion.p>

            {/* Description — subtle gray per design spec */}
            <motion.p {...riseIn(0.25)} className="mt-4 whitespace-pre-line leading-relaxed text-slate-400">
              {product.description}
            </motion.p>

            {/* Stock indicator */}
            <motion.div {...riseIn(0.3)} className="mt-5 flex items-center gap-2 text-sm font-semibold">
              {inStock ? (
                <>
                  <FiCheck className="text-emerald-500" />
                  <span className="text-emerald-600">In stock</span>
                  <span className="text-slate-500">· ships in 48h</span>
                </>
              ) : (
                <span className="text-red-500">Out of stock</span>
              )}
            </motion.div>

            {/* Qty selector + Add-to-cart CTA */}
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
                  
                  <button
                    onClick={() => dispatch(toggleWishlist(product.id))}
                    className={lex h-14 w-14 shrink-0 items-center justify-center rounded-2xl border transition-all }
                    aria-label="Toggle wishlist"
                  >
                    <FiHeart className={isWishlisted ? 'fill-current' : ''} size={22} />
                  </button>
                </>
              ) : (
                <button disabled className="btn-primary flex-1 !py-3.5 !text-base !bg-slate-800 !text-slate-500 !cursor-not-allowed">
                  Out of Stock
                </button>
              )}
              <button
                onClick={() => dispatch(toggleWishlist(product.id))}
                className={`flex w-14 items-center justify-center rounded-2xl border transition-all ${isWishlisted ? 'border-rose-500/50 bg-rose-500/10 text-rose-500 hover:bg-rose-500/20' : 'border-slate-700 bg-slate-800 text-slate-400 hover:border-slate-600 hover:text-slate-300'}`}
                aria-label="Toggle Wishlist"
              >
                <FiHeart size={20} className={isWishlisted ? "fill-rose-500" : ""} />
              </button>
            </motion.div>

            {/* Trust badges */}
            <motion.div {...riseIn(0.4)} className="mt-7 flex flex-wrap gap-x-6 gap-y-2 text-xs font-semibold text-slate-500">
              <span className="flex items-center gap-1.5">
                <FiTruck />
                {`Free shipping over ${formatPrice(150, currency, rates)}`}
              </span>
              <span className="flex items-center gap-1.5"><FiCheck /> 30-day returns</span>
            </motion.div>
          </div>
        </div>

                {/* ================= Reviews ================= */}
        <section className="mt-20 border-t border-slate-800 pt-16">
          <div className="flex items-center gap-3 mb-10">
            <FiMessageSquare className="text-indigo-400" size={28} />
            <h2 className="text-3xl font-black tracking-tight text-slate-100">Customer Reviews</h2>
          </div>

          <div className="grid gap-10 lg:grid-cols-3">
            {/* Review Form */}
            <div className="lg:col-span-1">
              <div className="bg-slate-800/30 border border-slate-700/50 p-6 rounded-3xl">
                <h3 className="text-xl font-bold text-slate-200 mb-4">Write a Review</h3>
                {user ? (
                  product?.reviews?.some(r => r.user_email === user.email) ? (
                    <div className="bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-sm p-4 rounded-xl flex items-start gap-3">
                      <FiCheck className="mt-0.5 shrink-0" />
                      <p>You have already reviewed this product. Thank you for your feedback!</p>
                    </div>
                  ) : (
                    <form onSubmit={submitReview} className="space-y-4">
                      <div>
                        <label className="block text-sm font-semibold text-slate-400 mb-2">Rating</label>
                        <div className="flex gap-2">
                          {[1, 2, 3, 4, 5].map((star) => (
                            <button
                              key={star}
                              type="button"
                              onClick={() => setRating(star)}
                              className="focus:outline-none transition-transform hover:scale-110"
                            >
                              <FiStar size={24} className={star <= rating ? "fill-amber-400 text-amber-400" : "text-slate-600"} />
                            </button>
                          ))}
                        </div>
                      </div>
                      <div>
                        <label className="block text-sm font-semibold text-slate-400 mb-2">Comment</label>
                        <textarea
                          value={comment}
                          onChange={(e) => setComment(e.target.value)}
                          rows="4"
                          placeholder="What did you like or dislike?"
                          className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-sm text-slate-200 placeholder-slate-500 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all resize-none"
                          required
                        />
                      </div>
                      <button
                        type="submit"
                        disabled={reviewLoading}
                        className="w-full btn-primary !py-3"
                      >
                        {reviewLoading ? "Submitting..." : "Submit Review"}
                      </button>
                    </form>
                  )
                ) : (
                  <div className="bg-slate-900 border border-slate-700 text-slate-400 text-sm p-4 rounded-xl">
                    <p className="mb-3">You need to be logged in to leave a review.</p>
                    <Link to="/login" className="btn-outline w-full block text-center !py-2">Sign In</Link>
                  </div>
                )}
              </div>
            </div>

            {/* Review List */}
            <div className="lg:col-span-2">
              {product.reviews?.length > 0 ? (
                <div className="grid gap-4 sm:grid-cols-2">
                  {product.reviews.map((r, i) => (
                    <motion.article
                      key={r.id}
                      initial={{ opacity: 0, y: 18 }}
                      whileInView={{ opacity: 1, y: 0 }}
                      viewport={{ once: true }}
                      transition={{ duration: 0.35, delay: (i % 4) * 0.07 }}
                      className="bg-slate-800/40 border border-slate-700/50 p-6 rounded-2xl flex flex-col h-full"
                    >
                      <div className="mb-4 flex items-center justify-between">
                        <span className="flex items-center gap-3 text-sm font-bold text-slate-200">
                          <span className="flex h-10 w-10 items-center justify-center rounded-full bg-indigo-500/20 text-indigo-400 uppercase">
                            {r.user_email.slice(0, 2)}
                          </span>
                          {r.user_email.split('@')[0]}
                        </span>
                        <span className="flex gap-0.5">
                          {[...Array(5)].map((_, s) => (
                            <FiStar key={s} size={14} className={s < r.rating ? "fill-amber-400 text-amber-400" : "fill-slate-700 text-slate-700"} />
                          ))}
                        </span>
                      </div>
                      <p className="text-sm leading-relaxed text-slate-300 flex-grow">{r.comment}</p>
                      <p className="text-xs text-slate-500 mt-4 pt-4 border-t border-slate-700/50">
                        {new Date(r.created_at).toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' })}
                      </p>
                    </motion.article>
                  ))}
                </div>
              ) : (
                <div className="flex flex-col items-center justify-center h-full min-h-[250px] bg-slate-800/20 rounded-3xl border border-slate-700/50 text-center p-8">
                  <div className="w-16 h-16 bg-slate-800 rounded-full flex items-center justify-center mb-4">
                    <FiStar className="text-slate-500" size={24} />
                  </div>
                  <h3 className="text-lg font-bold text-slate-300 mb-1">No reviews yet</h3>
                  <p className="text-sm text-slate-500 max-w-sm">Be the first to share your thoughts about this product.</p>
                </div>
              )}
            </div>
          </div>
        </section>
      </div>
    </PageTransition>
  );
}

