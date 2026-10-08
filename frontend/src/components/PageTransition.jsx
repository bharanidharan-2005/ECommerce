/**
 * PageTransition — wraps each routed page in a Framer Motion fade/slide.
 * Used together with <AnimatePresence mode="wait"> around <Routes> in App.jsx
 * so the outgoing page animates out before the incoming one animates in.
 */
import { motion } from "framer-motion";

export default function PageTransition({ children }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 14 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      transition={{ duration: 0.28, ease: "easeOut" }}
    >
      {children}
    </motion.div>
  );
}
