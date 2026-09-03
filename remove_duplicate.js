const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const originalLength = bookData.pages.length;
bookData.pages = bookData.pages.filter(p => p.title !== '연필로 설계를 할때');

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log(`Removed ${originalLength - bookData.pages.length} duplicate page(s).`);

