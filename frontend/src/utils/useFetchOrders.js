import { useCallback, useEffect, useState } from "react";
import api from "../api/axios";

/**
 * Fetches the signed-in user's order history.
 * Exposes `refresh` so UI (e.g. the tracking Refresh button) can re-poll
 * /api/orders/my/ without remounting the component.
 */
export default function useFetchOrders() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);

  const load = useCallback(() => {
    setLoading(true);
    let active = true;
    api
      .get("/orders/my/")
      .then(({ data }) => active && setOrders(Array.isArray(data) ? data : (data && Array.isArray(data.results) ? data.results : [])))
      .finally(() => active && setLoading(false));
    return () => {
      active = false;
    };
  }, []);

  useEffect(() => load(), [load]);

  return { orders, loading, refresh: load };
}
