const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

bookData.pages.forEach(p => {
    if (p.title && p.title.includes('다시, 신발을 신다 (에필로그)')) {
        p.text = p.text.replace(/스스로를 성찰하고, 타인을 포용하며, 현장의 불완전함을 껴안는 여정\./, 
            "조율자로서 흔들리지 않는 중심을 잡고, 서로 다른 욕망들을 둥글게 담아내며, 회의 테이블이라는 거대한 이해관계의 이면을 꿰뚫어 보는 여정.");
    }
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
