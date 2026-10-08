import os

filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\ProductListPage.jsx"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

old_effect = """  useEffect(() => {
    const urlCategory = searchParams.get("category");
    if (urlCategory) {
      if (urlCategory === "all") {
        setCategory("");
      } else {
        // If it's a name from the homepage, we need to match it to an ID later or assume it's already an ID.
        // The homepage passes category_name like `category=Electronics`. 
        // Our API expects category ID? Wait, does the API filter by category ID or name?
      }
    }
  }, [searchParams]);"""

new_effect = """  useEffect(() => {
    const urlCategory = searchParams.get("category");
    if (urlCategory && categoriesList.length > 1) {
      if (urlCategory === "all") {
        setCategory("");
      } else {
        const matched = categoriesList.find(c => c.name.toLowerCase() === urlCategory.toLowerCase() || String(c.id) === urlCategory);
        if (matched) {
          setCategory(matched.id);
        }
      }
    }
  }, [searchParams, categoriesList]);"""

content = content.replace(old_effect, new_effect)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated ProductListPage to resolve category names to IDs")
