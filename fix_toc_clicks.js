const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

html = html.replace('class="icon-btn toc-btn"', 'class="icon-btn toc-btn" onclick="openTOC()"');
html = html.replace('class="icon-btn close-toc-btn"', 'class="icon-btn close-toc-btn" onclick="closeTOC()"');
html = html.replace('class="toc-overlay"', 'class="toc-overlay" onclick="closeTOC()"');

html = html.replace(/v=20241108/g, 'v=20241109');

fs.writeFileSync('index.html', html, 'utf8');
