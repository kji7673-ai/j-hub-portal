const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

// Replace standard UI blues with dark gray/black
html = html.replace(/#0066cc/g, '#1d1d1f');
html = html.replace(/#0071e3/g, '#333333');

fs.writeFileSync('index.html', html, 'utf8');
