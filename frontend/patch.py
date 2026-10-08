import sys

with open('src/App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

imports_to_add = '''import AdminLayout from "./pages/admin/AdminLayout.jsx";
import AdminDashboard from "./pages/admin/AdminDashboard.jsx";
import AdminOrders from "./pages/admin/AdminOrders.jsx";
import AdminProducts from "./pages/admin/AdminProducts.jsx";'''

routes_to_add = '''
            {/* Admin Routes */}
            <Route
              path="/admin"
              element={
                <ProtectedRoute requireAdmin={true}>
                  <AdminLayout />
                </ProtectedRoute>
              }
            >
              <Route index element={<AdminDashboard />} />
              <Route path="orders" element={<AdminOrders />} />
              <Route path="products" element={<AdminProducts />} />
            </Route>
'''

content = content.replace('import RegisterPage from "./pages/RegisterPage.jsx";', 'import RegisterPage from "./pages/RegisterPage.jsx";\n' + imports_to_add)
content = content.replace('<Route path="*" element={<NotFoundPage />} />', routes_to_add + '\n            <Route path="*" element={<NotFoundPage />} />')

with open('src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
