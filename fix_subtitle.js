const fs = require('fs');

let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

bookData.pages.forEach(p => {
    if (p.title === '공유결합의 두 번째 질문: 서로 다른 욕망의 포용') {
        p.title = "공유결합의 두 번째 질문: 서로 다름을 이해하는 것";
        p.text = p.text.replace(/서로 다른 욕망과 결핍을 포용하는 과정입니다\./g, 
            "서로 다름을 이해하고, 그 다름이 가진 결핍을 귀중하게 담아내는 과정입니다.");
    }
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');

