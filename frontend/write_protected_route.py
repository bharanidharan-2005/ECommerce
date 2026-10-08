lines = [
    'import { Navigate, useLocation } from "react-router-dom";',
    'import { useSelector } from "react-redux";',
    '',
    'const ProtectedRoute = ({ children, requireAdmin = false }) => {',
    '  const { user } = useSelector((state) => state.auth);',
    '  const location = useLocation();',
    '',
    '  // If no user is logged in at all, redirect to login',
    '  if (!user) {',
    '    const next = encodeURIComponent(location.pathname + location.search);',
    '    return <Navigate to={/login?next=} replace />;',
    '  }',
    '',
    '  // If admin is required but user is not staff, redirect to homepage',
    '  if (requireAdmin && !user.is_staff) {',
    '    return <Navigate to="/" replace />;',
    '  }',
    '',
    '  // User is authorized',
    '  return children;',
    '};',
    '',
    'export default ProtectedRoute;'
]
with open('src/components/ProtectedRoute.jsx', 'w') as f:
    f.write('\\n'.join(lines))
