import { useSelector } from "react-redux";
import { Link } from "react-router-dom";
import { FiHeart, FiShoppingBag } from "react-icons/fi";
import { motion } from "framer-motion";

import PageTransition from "../components/PageTransition.jsx";
import BentoProductCard from "../components/BentoProductCard.jsx";
import EmptyState from "../components/ui/EmptyState.jsx";
import { selectWishlistItems } from "../features/products/wishlistSlice";

export default function WishlistPage() {
  const items = useSelector(selectWishlistItems) || [];

  return (
    <PageTransition>
      <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6">
        <h1 className="mb-8 flex items-center gap-3 text-3xl font-black tracking-tight sm:text-4xl">
          <FiHeart className="text-rose-500" /> My Wishlist
        </h1>

        {items.length === 0 ? (
          <EmptyState 
             title="Your wishlist is empty"
             message="Save your favorite items here while you shop."
             actionText="Continue Shopping"
             actionLink="/products"
          />
        ) : (
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {items.map((item, i) => (
              item.product_details ? (
                <BentoProductCard
                  key={item.id}
                  product={item.product_details}
                  variant="wishlist"
                  index={i}
                />
              ) : null
            ))}
          </div>
        )}
      </div>
    </PageTransition>
  );
}

