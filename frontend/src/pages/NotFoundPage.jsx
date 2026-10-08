/**
 * NotFoundPage — friendly 404 in the same floating-card language.
 */
import { Link } from "react-router-dom";
import { motion } from "framer-motion";

import PageTransition from "../components/PageTransition.jsx";

export default function NotFoundPage() {
  return (
    <PageTransition>
      <div className="mx-auto max-w-lg px-4 py-28 text-center">
        <motion.h1
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ type: "spring", stiffness: 200, damping: 14 }}
          className="text-7xl font-black tracking-tight text-indigo-400"
        >
          404
        </motion.h1>
        <p className="mt-5 text-slate-400">
          That page wandered off. Let's get you back to the good stuff.
        </p>
        <Link to="/" className="btn-primary mt-8">Back to Home</Link>
      </div>
    </PageTransition>
  );
}
