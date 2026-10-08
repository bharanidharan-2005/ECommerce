import os
import re

file_path = r'C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\ProductListPage.jsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the initial state
content = content.replace(
    'const [ordering, setOrdering] = useState("");',
    'const [ordering, setOrdering] = useState(searchParams.get("sort") || (searchParams.get("sale") === "true" ? "price" : ""));'
)

# Replace the category useEffect with a comprehensive one
old_effect = '''  useEffect(() => {
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
  }, [searchParams, categoriesList]);'''

new_effect = '''  useEffect(() => {
    const urlSearch = searchParams.get("search") || "";
    const urlSort = searchParams.get("sort");
    const urlSale = searchParams.get("sale");
    const urlCategory = searchParams.get("category");

    setSearch(urlSearch);

    if (urlSort) {
      setOrdering(urlSort);
    } else if (urlSale === "true") {
      setOrdering("price");
    } else {
      setOrdering("");
    }

    if (urlCategory && categoriesList.length > 1) {
      if (urlCategory === "all") {
        setCategory("");
      } else {
        const matched = categoriesList.find(c => c.name.toLowerCase() === urlCategory.toLowerCase() || String(c.id) === urlCategory);
        if (matched) {
          setCategory(matched.id);
        } else {
          setCategory("");
        }
      }
    } else if (!urlCategory) {
      setCategory("");
    }
  }, [searchParams, categoriesList]);'''

content = content.replace(old_effect, new_effect)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("ProductListPage patched successfully")