const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

let changeCount = 0;

bookData.pages.forEach(p => {
    if (p.text && p.text.includes('[저자의 메모]')) {
        p.text = p.text.replace(/<strong>\[저자의 메모\]<\/strong><br>\n?/g, '');
        p.text = p.text.replace(/\[저자의 메모\]/g, '');
        changeCount++;
    }
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log(`Removed labels from ${changeCount} pages.`);
