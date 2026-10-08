content = '''/**
 * ProtectedRoute - gate for authenticated-only pages.
 */
import { Navigate, useLocation } from "react-router-dom";
import { useSelector } from "react-redux";

export default function ProtectedRoute({ children, requireAdmin = false }) {
  const { user } = useSelector((s) => s.auth);
  const location = useLocation();

  if (!user) {
    const next = encodeURIComponent(location.pathname + location.search);
    return <Navigate to={\/login?next=\\} replace />;
  }

  if (requireAdmin && !user.is_staff) {
    return <Navigate to="/" replace />;
  }

  return children;
}
'''
with open('src/components/ProtectedRoute.jsx', 'w') as f:
    f.write(content)
