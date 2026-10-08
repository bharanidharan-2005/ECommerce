file_path = 'src/pages/ProductDetailPage.jsx'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

import_str = """import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { motion } from "framer-motion";
import { FiArrowLeft, FiCheck, FiShoppingBag, FiStar, FiTruck, FiHeart, FiMessageSquare } from "react-icons/fi";
import { toast } from "react-toastify";

import api from "../api/axios";
"""

content = content.replace('import { useEffect, useState } from "react";\nimport { Link, useParams } from "react-router-dom";\nimport { useDispatch, useSelector } from "react-redux";\nimport { motion } from "framer-motion";\nimport { FiArrowLeft, FiCheck, FiShoppingBag, FiStar, FiTruck, FiHeart } from "react-icons/fi";', import_str)

vars_str = """  const { id } = useParams();
  const dispatch = useDispatch();
  const { current: product, detailLoading } = useSelector((s) => s.products);
  const { user } = useSelector((s) => s.auth);
  const [qty, setQty] = useState(1);
  const currency = useSelector(selectCurrency);
  const { rates } = useSelector(selectProducts);
  
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
"""

content = content.replace('  const { id } = useParams();\n  const dispatch = useDispatch();\n  const { current: product, detailLoading } = useSelector((s) => s.products);\n  const [qty, setQty] = useState(1);\n  const currency = useSelector(selectCurrency);\n  const { rates } = useSelector(selectProducts);', vars_str)

reviews_str = """        {/* ================= Reviews ================= */}
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
        </section>"""

# Replace the old reviews section entirely
start_idx = content.find('{/* ================= Reviews ================= */}')
if start_idx != -1:
    end_idx = content.find('</div>\n    </PageTransition>', start_idx)
    content = content[:start_idx] + reviews_str + "\n      " + content[end_idx:]

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Successfully updated ProductDetailPage.jsx with Reviews section')
