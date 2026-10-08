const fs = require('fs');
let c = fs.readFileSync('src/features/products/productsSlice.js', 'utf8');
c = c.replace(/const symbols = \{[^}]+\};/, 'const symbols = { USD: "$", EUR: "€", GBP: "£", INR: "?", CAD: "$" };');
fs.writeFileSync('src/features/products/productsSlice.js', c);
