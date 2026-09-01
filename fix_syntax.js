const fs = require('fs');
const indexPath = 'index.html';

let content = fs.readFileSync(indexPath, 'utf8');

// The broken string is: 
// alt=".replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');"
// We want it to be alt="$1" ... wait, the JS string in index.html needs to actually say $1.
// So we just replace that exact broken string with '$1'
content = content.replace(/alt="\.replace\(\/\\\*\\\*\(\.\*\?\)\\\*\\\*\/g, '<strong>\$1<\/strong>'\);"/g, 'alt="$1"');

fs.writeFileSync(indexPath, content, 'utf8');
console.log("Syntax fixed.");
