const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const originalLength = bookData.pages.length;
bookData.pages = bookData.pages.filter(p => {
    let t1 = p.title && p.title.includes("수박으로 시대의 흐름을 판별하는");
    let t2 = p.title && p.title.includes("필연의 신은 누구인가요");
    return !(t1 || t2);
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log(`Deleted ${originalLength - bookData.pages.length} pages.`);
