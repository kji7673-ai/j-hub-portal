const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

bookData.pages.forEach(p => {
    // Check titles and text for "반응기" and replace with "무대"
    if (p.title && p.title.includes('현장이라는 반응기')) {
        p.title = p.title.replace('반응기', '무대');
    }
    
    if (p.text && p.text.includes('반응기')) {
        p.text = p.text.replace(/반응기/g, '무대');
    }
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');

