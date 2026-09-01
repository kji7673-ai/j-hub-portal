const fs = require('fs');
const indexPath = 'index.html';
let content = fs.readFileSync(indexPath, 'utf8');

// Use a simple split and join to replace the exact broken string
let parts = content.split('alt=".replace(/\\*\\*(.*?)\\*\\*/g, \\\'<strong>$1</strong>\\\');"');
content = parts.join('alt="$$1"'); // Note: In JavaScript string replacement $$ means literal $

fs.writeFileSync(indexPath, content, 'utf8');
console.log("Replaced broken string.");
