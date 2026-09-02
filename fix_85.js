const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

bookData.pages.forEach(p => {
    if (p.text && p.text.includes('85개')) {
        p.text = p.text.replace(/85개의 조각들은/g, "수십 편의 조각들은")
                       .replace(/이 85개의 기록에는/g, "이 거칠고 솔직한 기록들에는")
                       .replace(/85개의 기록/g, "수십 편의 기록");
    }
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log('Fixed 85 references.');
