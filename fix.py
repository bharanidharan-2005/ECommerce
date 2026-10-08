file_path = 'frontend/src/pages/HomePage.jsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    'import React, { useEffect } from "react";', 
    'import React, { useEffect, useState } from "react";'
)

hook_str = '''
  const [promotion, setPromotion] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8000/api/products/promotions/active/')
      .then(res => {
        if (!res.ok) throw new Error('No active promotion');
        return res.json();
      })
      .then(data => setPromotion(data))
      .catch(err => {
        console.log(err.message);
        setPromotion(null);
      });
  }, []);
'''

content = content.replace(
    'const { items: products, loading } = useSelector(selectProducts);',
    'const { items: products, loading } = useSelector(selectProducts);' + hook_str
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed HomePage.jsx')
