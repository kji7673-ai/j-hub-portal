const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

for (let p of bookData.pages) {
    if (p.title && p.title.match(/^\[성찰 \d-\d\] /)) {
        p.title = p.title.replace(/^\[성찰 \d-\d\] /, '');
    }
}

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log("Removed [성찰] prefixes from titles.");
