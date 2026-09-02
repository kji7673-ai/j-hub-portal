const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const originalLength = bookData.pages.length;
bookData.pages = bookData.pages.filter(p => {
    let titleMatch = p.title && p.title.includes("단두리");
    let textMatch = p.text && p.text.includes("단두리");
    return !(titleMatch || textMatch);
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log(`Deleted ${originalLength - bookData.pages.length} pages.`);
