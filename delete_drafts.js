const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const titlesToDelete = [
    "작아진 남자",
    "맘이",
    "나랑 같이 놀든이가",
    "가끔 나에게 실망을 했다는 사람들을 본다"
];

const initialCount = bookData.pages.length;

bookData.pages = bookData.pages.filter(p => !titlesToDelete.includes(p.title));

const finalCount = bookData.pages.length;

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');

console.log(`Deleted ${initialCount - finalCount} pages.`);
