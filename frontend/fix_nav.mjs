import fs from 'fs';
let c = fs.readFileSync('src/components/Navbar.jsx', 'utf8');
c = c.replace(/navigate\(\/products\\\?search=\);/, 'navigate(/products?search=\);');
fs.writeFileSync('src/components/Navbar.jsx', c);
