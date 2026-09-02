const fs = require('fs');
let code = fs.readFileSync('book_data.js', 'utf8');
code = code.replace('const bookData =', 'var bookData =');
eval(code);

bookData.pages[11].image = 'static/images/seogye_dong_1.png';

const newCode = `const bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', newCode, 'utf8');
console.log("Updated image for page 11");
