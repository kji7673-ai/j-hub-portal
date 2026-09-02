const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

bookData.pages.forEach(p => {
    if (p.title === "프롤로그: 완벽한 시스템이 아닌, 불완전한 쟁이의 생존기") {
        p.title = "프롤로그: 건축 외에는 아무것도 모르는 바보의 이야기";
    }
    if (p.title === "프롤로그: 완벽한 시스템이 아닌, 불완전한 쟁이의 생존기 (계속)") {
        p.title = "프롤로그: 건축 외에는 아무것도 모르는 바보의 이야기 (계속)";
    }
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
