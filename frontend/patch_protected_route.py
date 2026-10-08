import sys

with open('src/components/ProtectedRoute.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('to={/login?next=}', 'to={/login?next=}')

with open('src/components/ProtectedRoute.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
