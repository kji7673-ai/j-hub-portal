const fs = require('fs');
let code = fs.readFileSync('book_data.js', 'utf8');
code = code.replace('var bookData =', 'const bookData =');
// wait, it's currently var or const? Let's just use eval.
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const newPages = bookData.pages.filter(p => {
    if (p.title && p.title.includes('깊어지는 질문들')) {
        return false;
    }
    return true;
});

bookData.pages = newPages;

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log("Removed duplicated bridges. Remaining pages:", newPages.length);
