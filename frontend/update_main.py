import os

filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\main.jsx"

with open(filepath, "r") as f:
    content = f.read()

if "SettingsProvider" not in content:
    content = content.replace("import App from \"./App.jsx\";", "import App from \"./App.jsx\";\nimport { SettingsProvider } from \"./context/SettingsContext.jsx\";")
    content = content.replace("<App />", "<SettingsProvider>\n          <App />\n        </SettingsProvider>")
    
    with open(filepath, "w") as f:
        f.write(content)
    print("Updated main.jsx")
else:
    print("main.jsx already updated")
