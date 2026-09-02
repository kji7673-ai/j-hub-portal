const fs = require('fs');
let code = fs.readFileSync('book_data.js', 'utf8');
code = code.replace('const bookData =', 'var bookData =');
eval(code);

if (bookData.pages[1].type !== 'author_profile') {
    bookData.pages.splice(1, 0, { type: 'author_profile' });
}

const newCode = `const bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', newCode, 'utf8');
console.log("Added author_profile back to book_data.js");
