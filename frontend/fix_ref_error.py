import os

filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\ProductListPage.jsx"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# First, remove the misplaced useEffect
bad_effect = """  useEffect(() => {
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

content = content.replace(bad_effect, "")

# Now add it AFTER categoriesList is defined
target = 'const [categoriesList, setCategoriesList] = useState([{ id: "", name: "All Collections" }]);'
good_effect = target + "\n\n" + bad_effect

content = content.replace(target, good_effect)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed categoriesList ReferenceError")
