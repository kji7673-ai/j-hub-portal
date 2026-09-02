const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

const originalLength = bookData.pages.length;
bookData.pages = bookData.pages.filter(p => {
    let isCover = p.type === 'cover' && p.title === 'Y구역 현장 기록' && p.image === 'static/images/09.jpg';
    let isPage1 = p.title === '완벽한 보고서의 패배: 심의와 설득의 기술';
    let isPage2 = p.title === '서류 완벽주의의 함정: 타당성 검토의 배신';
    return !(isCover || isPage1 || isPage2);
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
console.log(`Deleted ${originalLength - bookData.pages.length} pages.`);
