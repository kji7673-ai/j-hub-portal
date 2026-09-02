const fs = require('fs');
let code = fs.readFileSync('book_data.js', 'utf8');
let dataCode = code.replace(/const bookData =|var bookData =/g, 'global.bookData =');
eval(dataCode);

bookData.pages.forEach(p => {
    if (p.title === "중간 장. 기계를 거부하지 않기로 결심한 날") {
        p.type = "interlude";
        p.image = "static/images/interlude_part3_clean.jpg";
    }
    if (p.title === "제4장. 다시, 신발을 신다 (에필로그)") {
        p.type = "interlude";
        p.image = "static/images/interlude_part4_clean.jpg";
    }
});

const outCode = `var bookData = ${JSON.stringify(bookData, null, 4)};\n\nif (typeof module !== 'undefined' && module.exports) {\n    module.exports = bookData;\n}\n`;
fs.writeFileSync('book_data.js', outCode, 'utf8');
