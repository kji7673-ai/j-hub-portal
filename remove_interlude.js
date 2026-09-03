const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

// Filter out the redundant middle chapter
const originalLength = bookData.pages.length;
bookData.pages = bookData.pages.filter(p => p.title !== '중간 장. 기계를 거부하지 않기로 결심한 날');

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log(`Removed ${originalLength - bookData.pages.length} page(s).`);

