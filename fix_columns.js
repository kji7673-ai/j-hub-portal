const fs = require('fs');
const indexPath = 'index.html';

let content = fs.readFileSync(indexPath, 'utf8');

// Remove all column-width, column-gap, column-count so it just scrolls vertically
content = content.replace(/column-width:\s*[^;]+;/g, '');
content = content.replace(/column-gap:\s*[^;]+;/g, '');
content = content.replace(/column-count:\s*[^;!]+(!important)?;/g, '');

fs.writeFileSync(indexPath, content, 'utf8');
console.log("Columns removed.");
