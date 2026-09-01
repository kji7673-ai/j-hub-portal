const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

html = html.replace("window.addEventListener('DOMContentLoaded', () => {\n    try {", "window.addEventListener('DOMContentLoaded', () => {");
fs.writeFileSync('index.html', html, 'utf8');
console.log("Removed broken try-catch.");
