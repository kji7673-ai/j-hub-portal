const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

html = html.replace("pageEl.style.position = 'relative';", "/* removed position: relative to prevent height collapse */ pageEl.style.height = '100%';");

fs.writeFileSync('index.html', html, 'utf8');
console.log("Fixed cover height collapse!");
