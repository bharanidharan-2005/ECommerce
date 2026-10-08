import ast
import astunparse

with open(r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\apps\orders\views.py', 'r', encoding='utf-8') as f:
    code = f.read()

tree = ast.parse(code)
for node in ast.walk(tree):
    if isinstance(node, ast.ClassDef) and node.name == 'CheckoutView':
        for child in node.body:
            if isinstance(child, ast.FunctionDef) and child.name == 'post':
                print(astunparse.unparse(child))