import os
import re

app_path = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\App.jsx'
with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add import
import_pattern = r'import CartDrawer from "./components/ui/CartDrawer\.jsx";'
new_import = '''import CartDrawer from "./components/ui/CartDrawer.jsx";
import WelcomePopup from "./components/WelcomePopup.jsx";'''
content = content.replace('import CartDrawer from "./components/ui/CartDrawer.jsx";', new_import)

# Add component
comp_pattern = r'<CartDrawer />\s*</div>\s*\);\s*}'
new_comp = '''<CartDrawer />
      {!location.pathname.startsWith("/admin") && <WelcomePopup />}
    </div>
  );
}'''
content = re.sub(comp_pattern, new_comp, content)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("App.jsx patched.")