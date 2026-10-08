import os

filepath = r"C:\Users\M.BHARANIDHARAN\OneDrive\Documents\ECommerce\frontend\src\pages\ProductListPage.jsx"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Add useSearchParams to imports
if "useSearchParams" not in content:
    content = content.replace('import { Link } from "react-router-dom";', 'import { Link, useSearchParams } from "react-router-dom";')
    # If Link is not there, just put it after react-icons
    if "useSearchParams" not in content:
        content = content.replace('import { motion, AnimatePresence } from "framer-motion";', 'import { motion, AnimatePresence } from "framer-motion";\nimport { useSearchParams } from "react-router-dom";')

# Add initialization inside the component
old_state = """  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");
  const [ordering, setOrdering] = useState("");"""

new_state = """  const [searchParams, setSearchParams] = useSearchParams();
  const [search, setSearch] = useState(searchParams.get("search") || "");
  const [category, setCategory] = useState(searchParams.get("category") && searchParams.get("category") !== "all" ? searchParams.get("category") : "");
  const [ordering, setOrdering] = useState("");

  useEffect(() => {
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

content = content.replace(old_state, new_state)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated ProductListPage to use searchParams")
