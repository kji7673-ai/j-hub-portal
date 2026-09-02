const fs = require('fs');
let code = fs.readFileSync('book_data.js', 'utf8');
code = code.replace('const bookData =', 'var bookData =');
eval(code);

for (let p of bookData.pages) {
    if (p.title && p.title.includes('누가, 언제, 무엇을 하는가? (계속)')) {
        p.text = p.text.replace('</div>', '');
    }
}

const newCode = `const bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', newCode, 'utf8');
console.log("Fixed stray div");
