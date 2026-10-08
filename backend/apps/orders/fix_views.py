import os

filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\backend\apps\orders\views.py"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("from rest_framework import generics", "from rest_framework import generics, serializers")

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
print("Added serializers to views.py imports")
