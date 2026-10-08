file_path = 'src/App.jsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

import_str = """import { Navigate, Route, Routes, useLocation } from "react-router-dom";"""
if import_str in content:
    print("Found imports")
    
if '<Navbar />' in content:
    content = content.replace('<Navbar />', '{!location.pathname.startsWith("/admin") && <Navbar />}')
    print("Replaced Navbar")
    
if '<Footer />' in content:
    content = content.replace('<Footer />', '{!location.pathname.startsWith("/admin") && <Footer />}')
    print("Replaced Footer")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
