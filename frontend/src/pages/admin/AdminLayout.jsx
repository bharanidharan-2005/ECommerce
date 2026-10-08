import { useState, useEffect } from "react";
import { Outlet, NavLink, useNavigate, Link } from "react-router-dom";
import { 
  LayoutDashboard, ShoppingBag, Package, Users, BarChart2, 
  Settings, LogOut, Bell, Menu, X, Mail, Tag
} from "lucide-react";
import { useDispatch, useSelector } from "react-redux";
import { formatDistanceToNow } from "date-fns";
import { logout } from "../../features/auth/authSlice";
import api from "../../api/axios";

export default function AdminLayout() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { user } = useSelector((s) => s.auth);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isNotificationsOpen, setIsNotificationsOpen] = useState(false);
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [isProfileOpen, setIsProfileOpen] = useState(false);

  useEffect(() => {
    const fetchNotifications = async () => {
      try {
        const res = await api.get("/orders/admin/notifications/");
        setNotifications(res.data);
        setUnreadCount(res.data.filter(n => n.unread).length);
      } catch (err) {
        console.error("Failed to fetch notifications", err);
      }
    };
    fetchNotifications();
    
    // Refresh notifications every 60 seconds
    const interval = setInterval(fetchNotifications, 60000);
    return () => clearInterval(interval);
  }, []);

  const markAllAsRead = () => {
    setNotifications(notifications.map(n => ({ ...n, unread: false })));
    setUnreadCount(0);
  };


  const handleLogout = () => {
    dispatch(logout());
    navigate("/login");
  };

  const navItems = [
    { to: "/admin", icon: LayoutDashboard, label: "Dashboard", end: true },
    { to: "/admin/orders", icon: ShoppingBag, label: "Orders" },
    { to: "/admin/products", icon: Package, label: "Products" },
    { to: "/admin/customers", icon: Users, label: "Customers" },
    { to: "/admin/subscribers", icon: Mail, label: "Subscribers" },
    { to: "/admin/promos", icon: Tag, label: "Promos" },
    { to: "/admin/analytics", icon: BarChart2, label: "Analytics" },
  ];

  return (
    <div className="flex h-screen bg-slate-950 overflow-hidden text-slate-200">
      
      {/* Mobile Sidebar Overlay */}
      {isMobileMenuOpen && (
        <div 
          className="fixed inset-0 bg-black/60 z-40 lg:hidden"
          onClick={() => setIsMobileMenuOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside className={`fixed lg:static inset-y-0 left-0 z-50 w-64 border-r border-slate-800 bg-slate-900 transform transition-transform duration-300 lg:transform-none flex flex-col ${isMobileMenuOpen ? "translate-x-0" : "-translate-x-full"}`}>
        <div className="p-6 flex items-center justify-between">
          <div>
            <div className="text-xl font-black text-white tracking-tight">SHOPVERSE</div>
            <div className="text-xs font-semibold text-indigo-400 tracking-wider uppercase mt-1">Admin Panel</div>
          </div>
          <button className="lg:hidden text-slate-400 hover:text-white" onClick={() => setIsMobileMenuOpen(false)}>
            <X className="h-5 w-5" />
          </button>
        </div>

        <nav className="flex-1 px-4 py-4 space-y-1 overflow-y-auto">
          {navItems.map(({ to, icon: Icon, label, end }) => (
            <NavLink
              key={label}
              to={to}
              end={end}
              onClick={() => setIsMobileMenuOpen(false)}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors ${
                  isActive
                    ? "bg-indigo-500/10 text-indigo-400"
                    : "text-slate-400 hover:bg-slate-800 hover:text-slate-200"
                }`
              }
            >
              <Icon className="h-5 w-5" />
              {label}
            </NavLink>
          ))}
          
          <div className="my-4 border-t border-slate-800" />
          
          <NavLink
            to="/admin/settings"
            className="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium text-slate-400 transition-colors hover:bg-slate-800 hover:text-slate-200"
          >
            <Settings className="h-5 w-5" />
            Settings
          </NavLink>
          <button
            onClick={handleLogout}
            className="flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium text-slate-400 transition-colors hover:bg-slate-800 hover:text-rose-400"
          >
            <LogOut className="h-5 w-5" />
            Sign Out
          </button>
        </nav>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        
        {/* Top Navbar */}
        <header className="h-16 border-b border-slate-800 bg-slate-900/50 flex items-center justify-between px-4 lg:px-8">
          <div className="flex items-center gap-4">
            <button className="lg:hidden text-slate-400 hover:text-white" onClick={() => setIsMobileMenuOpen(true)}>
              <Menu className="h-6 w-6" />
            </button>
            <div className="text-lg font-bold text-white lg:hidden">ShopVerse Admin</div>
          </div>

          <div className="flex items-center gap-6">
            <Link to="/" className="hidden sm:block text-sm font-medium text-indigo-400 hover:text-indigo-300 transition-colors">
              View Store
            </Link>
            <div className="flex items-center gap-4">
              <div className="relative">
                <button 
                  onClick={() => setIsNotificationsOpen(!isNotificationsOpen)} 
                  className="text-slate-400 hover:text-white transition-colors relative"
                >
                  <Bell className="h-5 w-5" />
                  {unreadCount > 0 && (
                    <span className="absolute -top-1 -right-1 flex h-3 w-3 items-center justify-center rounded-full bg-rose-500 text-[10px] font-bold text-white">
                      {unreadCount}
                    </span>
                  )}
                </button>

                {isNotificationsOpen && (
                  <div className="absolute right-0 mt-2 w-80 origin-top-right rounded-lg border border-slate-700 bg-slate-800 py-2 shadow-xl z-50">
                    <div className="flex items-center justify-between px-4 pb-2 border-b border-slate-700">
                      <h3 className="text-sm font-semibold text-slate-200">Notifications</h3>
                      <button 
                        onClick={markAllAsRead}
                        className="text-xs text-indigo-400 hover:text-indigo-300"
                      >
                        Mark all as read
                      </button>
                    </div>
                    <div className="max-h-80 overflow-y-auto">
                      {notifications.length === 0 ? (
                        <div className="px-4 py-6 text-center text-slate-400 text-sm">No new notifications</div>
                      ) : (
                        notifications.map((notif) => (
                        <div key={notif.id} className={`px-4 py-3 hover:bg-slate-700/50 cursor-pointer ${notif.unread ? "bg-slate-800/80" : ""}`}>
                          <div className="flex items-start justify-between">
                            <p className={`text-sm font-medium ${notif.unread ? "text-slate-200" : "text-slate-400"}`}>
                              {notif.title}
                            </p>
                            <span className="text-xs text-slate-500">{formatDistanceToNow(new Date(notif.time), { addSuffix: true })}</span>
                          </div>
                          <p className="text-xs text-slate-400 mt-1">{notif.desc}</p>
                        </div>
                      ))
                      )}
                    </div>
                    <div className="border-t border-slate-700 px-4 pt-2">
                      <button 
                        onClick={() => { setIsNotificationsOpen(false); navigate("/admin/orders"); }}
                        className="w-full text-center text-sm font-medium text-indigo-400 hover:text-indigo-300 py-1"
                      >
                        View All Orders
                      </button>
                    </div>
                  </div>
                )}
              </div>
              
              <div className="h-6 w-px bg-slate-700 mx-1"></div>
              <div className="relative">
                <button 
                  onClick={() => setIsProfileOpen(!isProfileOpen)}
                  className="flex items-center gap-2 cursor-pointer group focus:outline-none"
                >
                  <div className="h-8 w-8 rounded-full bg-indigo-500/20 text-indigo-400 flex items-center justify-center font-bold text-sm">
                    {user?.name?.charAt(0) || "A"}
                  </div>
                  <div className="hidden sm:block text-sm font-medium text-slate-300 group-hover:text-white transition-colors">
                    {user?.name || "Admin"}  
                  </div>
                </button>
                {isProfileOpen && (
                  <div className="absolute right-0 mt-2 w-48 origin-top-right rounded-lg border border-slate-700 bg-slate-800 py-2 shadow-xl z-50">
                    <div className="px-4 py-2 border-b border-slate-700">
                      <p className="text-sm font-medium text-white">{user?.name || "Admin"}</p>
                      <p className="text-xs text-slate-400 truncate">{user?.email || "admin@shopverse.com"}</p>
                    </div>
                    <div className="py-1">
                      <Link to="/admin/settings" onClick={() => setIsProfileOpen(false)} className="block px-4 py-2 text-sm text-slate-300 hover:bg-slate-700 hover:text-white">My Profile</Link>
                      <Link to="/admin/settings" onClick={() => setIsProfileOpen(false)} className="block px-4 py-2 text-sm text-slate-300 hover:bg-slate-700 hover:text-white">Settings</Link>
                    </div>
                    <div className="border-t border-slate-700 py-1">
                      <button onClick={() => { setIsProfileOpen(false); handleLogout(); }} className="block w-full text-left px-4 py-2 text-sm text-rose-400 hover:bg-slate-700 hover:text-rose-300">Sign Out</button>
                    </div>
                  </div>
                )}
              </div>
            </div>

          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 overflow-y-auto p-4 lg:p-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
