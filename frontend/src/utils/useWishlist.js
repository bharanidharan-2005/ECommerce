import { useState, useEffect, useCallback } from "react";
import { useSelector } from "react-redux";
import api from "./api";

const useWishlist = () => {
  const [wishlist, setWishlist] = useState([]);
  const [loading, setLoading] = useState(false);
  const { user } = useSelector((s) => s.auth);

  const fetchWishlist = useCallback(async () => {
    if (!user) {
      setWishlist([]);
      return;
    }
    setLoading(true);
    try {
      const { data } = await api.get("/products/wishlist/");
      const items = Array.isArray(data) ? data : (data && Array.isArray(data.results) ? data.results : []);
      setWishlist(items);
    } catch (err) {
      console.error("Failed to fetch wishlist", err);
    } finally {
      setLoading(false);
    }
  }, [user]);

  useEffect(() => {
    fetchWishlist();
  }, [fetchWishlist]);

  const toggleWishlist = async (productId) => {
    if (!user) return; // Prompt login in real app
    const existing = wishlist.find((w) => w.product === productId);
    
    // Optimistic update
    if (existing) {
      setWishlist((prev) => prev.filter((w) => w.product !== productId));
      try {
        await api.delete(`/products/wishlist/${existing.id}/`);
      } catch (err) {
        // Revert
        fetchWishlist();
      }
    } else {
      // Optimistic update (fake ID)
      const fakeId = Date.now();
      setWishlist((prev) => [...prev, { id: fakeId, product: productId }]);
      try {
        const { data } = await api.post("/products/wishlist/", { product: productId });
        // Replace fake ID with real ID
        setWishlist((prev) => prev.map((w) => w.id === fakeId ? data : w));
      } catch (err) {
        // Revert
        fetchWishlist();
      }
    }
  };

  return { wishlist, loading, toggleWishlist, fetchWishlist };
};

export default useWishlist;
