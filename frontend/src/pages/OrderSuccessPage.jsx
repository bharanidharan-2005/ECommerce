/**
 * OrderSuccessPage â€” confirmation screen whose copy adapts to how the
 * shopper paid:
 *   ?method=cod        -> "keep cash ready at delivery" (order stays pending)
 *   ?method=upi_*      -> UPI collect request sent; status flips to paid
 *                         once approved in the app (webhook)
 *   default (card)     -> instant Stripe success message
 */
import { Link, useParams, useSearchParams } from "react-router-dom";
import { motion } from "framer-motion";

import PageTransition from "../components/PageTransition.jsx";

export default function OrderSuccessPage() {
  const { orderNumber } = useParams();
  const [params] = useSearchParams();
  const method = params.get("method") || "card";

  /** Per-method headline + detail copy */
  const COPY = {
    cod: {
      title: "Order placed!",
      detail: (
        <>
          Keep cash ready â€” you'll pay the courier the invoice amount on delivery.
          You can track the order anytime below.
        </>
      ),
    },
    upi_gpay: {
      title: "Almost there!",
      detail: (
        <>
          We've sent a collect request to your <b className="text-slate-100">Google Pay</b>.
          Approve it within 5 minutes â€” your order status flips to â€œpaidâ€ automatically.
        </>
      ),
    },
    upi_paytm: {
      title: "Almost there!",
      detail: (
        <>
          We've sent a collect request via <b className="text-slate-100">Paytm</b>. Approve it
          in the app and your order status will update instantly.
        </>
      ),
    },
    card: {
      title: "Thank you!",
      detail: (
        <>
          Your payment went through and order{" "}
          <b className="text-slate-100">#{orderNumber}</b> is being prepared for dispatch.
        </>
      ),
    },
  };
  const copy = COPY[method] ?? COPY.card;

  // Estimated delivery logic (approx 5-7 days)
  const deliveryDateStart = new Date();
  deliveryDateStart.setDate(deliveryDateStart.getDate() + 5);
  const deliveryDateEnd = new Date();
  deliveryDateEnd.setDate(deliveryDateEnd.getDate() + 7);
  const options = { weekday: 'short', month: 'short', day: 'numeric' };
  const estDelivery = `${deliveryDateStart.toLocaleDateString(undefined, options)} - ${deliveryDateEnd.toLocaleDateString(undefined, options)}`;

  return (
    <PageTransition>
      <div className="mx-auto max-w-lg px-4 py-24 sm:px-6">
        <motion.div
          initial={{ opacity: 0, y: 24, scale: 0.97 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          transition={{ duration: 0.45, ease: [0.22, 1, 0.36, 1] }}
          className="card p-10 text-center sm:p-14"
        >
          {/* Springing icon: check for settled payments, clock while awaiting COD/UPI */}
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: "spring", stiffness: 260, damping: 16, delay: 0.15 }}
            className={`mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-full ${
              method === "card" ? "bg-emerald-100 text-emerald-600" : "bg-indigo-100 text-indigo-400"
            }`}
          >
            {method === "card" ? (
              <svg viewBox="0 0 24 24" className="h-9 w-9" fill="none" stroke="currentColor" strokeWidth={2.5} strokeLinecap="round" strokeLinejoin="round">
                <path d="M20 6L9 17l-5-5" />
              </svg>
            ) : (
              <svg viewBox="0 0 24 24" className="h-9 w-9" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="10" />
                <path d="M12 6v6l4 2" />
              </svg>
            )}
          </motion.div>

          <h1 className="text-3xl font-black tracking-tight">{copy.title}</h1>
          <p className="mt-3 leading-relaxed text-slate-400">
            {method === "card" && <>Your payment went through and order </>}
            {method !== "card" && <>Order </>}
            <span className="font-extrabold text-slate-100">#{orderNumber}</span>{" "}
            is confirmed{method === "card" ? "." : " â€” awaiting your action."}
          </p>
          <p className="mt-2 text-sm text-slate-500">{copy.detail}</p>
          
          <div className="mt-6 p-4 rounded-xl bg-slate-800/50 border border-slate-700">
            <h3 className="text-sm font-bold text-slate-300 mb-1">Estimated Delivery</h3>
            <p className="text-lg font-extrabold text-indigo-400">{estDelivery}</p>
          </div>

          <div className="mt-9 flex flex-col gap-3 sm:flex-row sm:justify-center">
            <Link to="/profile" className="btn-primary">Track My Order</Link>
            <Link to="/products" className="btn-outline">Continue Shopping</Link>
          </div>
        </motion.div>
      </div>
    </PageTransition>
  );
}
