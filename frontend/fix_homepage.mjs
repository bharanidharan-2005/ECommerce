import fs from 'fs';
let c = fs.readFileSync('src/pages/HomePage.jsx', 'utf8');
c = c.replace(/over \\"/g, 'over "');
fs.writeFileSync('src/pages/HomePage.jsx', c);
