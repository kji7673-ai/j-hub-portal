const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

// Insert window.onload = renderBook; at the bottom of the script
html = html.replace('function openBookmarkList() {', 'window.onload = renderBook;\n\n        function openBookmarkList() {');

// Force bump version to break cache again
html = html.replace(/v=20241106/g, 'v=20241107');

fs.writeFileSync('index.html', html, 'utf8');
