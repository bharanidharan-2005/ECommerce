import sys

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    content = content.replace('return <Navigate to={/login?next=$' + '{next}} replace />;', 'return <Navigate to={/login?next=$' + '{next}} replace />;')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

fix_file('src/components/ProtectedRoute.jsx')
