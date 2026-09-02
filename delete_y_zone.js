const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const originalLength = bookData.pages.length;
bookData.pages = bookData.pages.filter(p => {
    let isCover = p.type === 'cover' && p.title === 'Y구역 현장 기록' && p.image === 'static/images/07.jpg';
    let isPage = p.title === 'AI가 읽지 못하는 지역 맥락: 달동네의 바람길';
    return !(isCover || isPage);
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log(`Deleted ${originalLength - bookData.pages.length} pages.`);
